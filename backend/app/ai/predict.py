"""
MediShield AI: Real-Time Shortage Prediction & SHAP Explainer
Module: backend.app.ai.predict

Generates shortage probability, risk categorization, and per-instance SHAP feature explanations.
Automatically transforms raw features into the 11-feature domain representation.
"""

import os
import sys
import joblib
import pandas as pd
import shap
from typing import Dict, Any

current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
backend_dir = os.path.dirname(app_dir)
root_dir = os.path.dirname(backend_dir)
for p in [current_dir, app_dir, backend_dir, root_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from .feature_engineering import compute_domain_features, ALL_FEATURE_COLUMNS, RAW_FEATURE_COLUMNS
except ImportError:
    from feature_engineering import compute_domain_features, ALL_FEATURE_COLUMNS, RAW_FEATURE_COLUMNS

MODEL_PATH = os.path.join(current_dir, "xgboost_model.pkl")

# Lazy-loaded global instances to allow training beforehand
_model = None
_explainer = None
_feature_names = None


def _get_model_and_explainer():
    global _model, _explainer, _feature_names
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Run train_model.py first.")
        artifact = joblib.load(MODEL_PATH)
        if isinstance(artifact, dict) and "model" in artifact:
            _model = artifact["model"]
            _feature_names = artifact.get("feature_names", ALL_FEATURE_COLUMNS)
        else:
            _model = artifact
            _feature_names = getattr(_model, "feature_names_in_", RAW_FEATURE_COLUMNS)
        _explainer = shap.TreeExplainer(_model)
    return _model, _explainer, _feature_names


def predict_shortage(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predicts medicine shortage probability and returns SHAP attributions.
    
    Args:
        features: dict with keys 'inventory', 'demand', 'lead_time',
                  'supplier_reliability', 'expiry_days', 'safety_stock'
    """
    model, explainer, feature_names = _get_model_and_explainer()

    df_raw = pd.DataFrame([features])
    
    # Add domain features if model was trained with them
    if len(feature_names) > len(RAW_FEATURE_COLUMNS):
        df_eval = compute_domain_features(df_raw)
        df_input = df_eval[feature_names]
    else:
        df_input = df_raw[feature_names]

    probability = float(model.predict_proba(df_input)[0][1])
    shap_vals = explainer(df_input)

    explanation = []
    vals = shap_vals.values[0] if len(shap_vals.values.shape) == 2 else shap_vals.values[0, :, 1]
    
    for name, value in zip(df_input.columns, vals):
        explanation.append({
            "feature": name,
            "impact": round(float(value), 3),
        })

    # Sort explanations by absolute impact
    explanation = sorted(
        explanation,
        key=lambda x: abs(x["impact"]),
        reverse=True,
    )

    if probability >= 0.75:
        risk = "High"
    elif probability >= 0.45:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "probability": round(probability * 100.0, 2),
        "risk": risk,
        "explanation": explanation[:6],
    }