"""
MediShield AI: Explainable AI (SHAP) Module
Module: backend.app.ai.shap_explain

Provides:
1. Global SHAP feature importance & beeswarm attribution.
2. Direction of influence analysis (Spearman / Pearson correlation).
3. Representative local explanation case selection (TP, TN, FP, FN).
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
import shap
from scipy.stats import pearsonr


def compute_global_shap_attributions(
    model,
    X_test: pd.DataFrame,
) -> Tuple[shap.Explanation, pd.DataFrame]:
    """
    Computes SHAP values on held-out test data using TreeExplainer.
    Returns:
        shap_explanation: shap.Explanation object
        df_importance: summary DataFrame with columns:
            Feature, Mean |SHAP|, Correlation r, Direction, Domain Interpretation
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test)

    # For binary classification, use positive class attribution
    if len(shap_values.values.shape) == 3:
        vals = shap_values.values[:, :, 1]
    else:
        vals = shap_values.values

    feature_names = X_test.columns.tolist()
    mean_abs_shap = np.mean(np.abs(vals), axis=0)

    rows = []
    for i, f_name in enumerate(feature_names):
        feature_data = X_test[f_name].values
        shap_col = vals[:, i]

        # Compute correlation between feature value and SHAP attribution
        if np.std(feature_data) > 1e-9 and np.std(shap_col) > 1e-9:
            r, _ = pearsonr(feature_data, shap_col)
        else:
            r = 0.0

        direction = "Positive (+)" if r > 0.05 else "Negative (-)" if r < -0.05 else "Non-linear / Mixed"
        
        # Domain interpretation
        if direction.startswith("Positive"):
            interp = f"Higher {f_name} is associated with increased model-predicted shortage output."
        elif direction.startswith("Negative"):
            interp = f"Higher {f_name} is associated with decreased model-predicted shortage output (protective)."
        else:
            interp = f"{f_name} demonstrates non-linear or threshold-dependent contribution."

        rows.append({
            "feature": f_name,
            "mean_abs_shap": round(float(mean_abs_shap[i]), 4),
            "correlation_r": round(float(r), 4),
            "direction": direction,
            "interpretation": interp,
        })

    df_importance = pd.DataFrame(rows).sort_values(by="mean_abs_shap", ascending=False).reset_index(drop=True)
    return shap_values, df_importance


def extract_representative_local_cases(
    model,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    shap_values: shap.Explanation,
) -> List[Dict[str, Any]]:
    """
    Selects 4 representative local explanation cases from held-out test set:
    1. True Positive (High Risk, Confirmed Shortage)
    2. True Negative (Low Risk, Confirmed No Shortage)
    3. False Positive (Model flagged shortage, actual no shortage)
    4. False Negative (Model failed to flag shortage, actual shortage)
    """
    y_true = y_test.values
    y_probs = model.predict_proba(X_test)[:, 1]
    y_preds = (y_probs >= 0.50).astype(int)

    if len(shap_values.values.shape) == 3:
        vals = shap_values.values[:, :, 1]
    else:
        vals = shap_values.values

    # Find candidate indices
    tp_indices = np.where((y_true == 1) & (y_preds == 1))[0]
    tn_indices = np.where((y_true == 0) & (y_preds == 0))[0]
    fp_indices = np.where((y_true == 0) & (y_preds == 1))[0]
    fn_indices = np.where((y_true == 1) & (y_preds == 0))[0]

    cases = []

    def build_case_dict(idx: int, case_type: str):
        row_vals = vals[idx]
        top_feat_idx = np.argsort(np.abs(row_vals))[::-1][:5]
        top_features = []
        for fi in top_feat_idx:
            top_features.append({
                "feature": X_test.columns[fi],
                "feature_value": float(X_test.iloc[idx, fi]),
                "shap_impact": round(float(row_vals[fi]), 4),
            })

        return {
            "case_type": case_type,
            "sample_index": int(idx),
            "true_label": int(y_true[idx]),
            "predicted_label": int(y_preds[idx]),
            "predicted_probability": round(float(y_probs[idx]), 4),
            "top_contributing_features": top_features,
            "all_features": {col: float(X_test.iloc[idx][col]) for col in X_test.columns},
            "all_shap_values": {col: round(float(row_vals[i]), 4) for i, col in enumerate(X_test.columns)},
        }

    # 1. High-confidence TP (highest probability among TPs)
    if len(tp_indices) > 0:
        best_tp = tp_indices[np.argmax(y_probs[tp_indices])]
        cases.append(build_case_dict(best_tp, "True Positive (High Risk)"))

    # 2. High-confidence TN (lowest probability among TNs)
    if len(tn_indices) > 0:
        best_tn = tn_indices[np.argmin(y_probs[tn_indices])]
        cases.append(build_case_dict(best_tn, "True Negative (Low Risk)"))

    # 3. False Positive (if present)
    if len(fp_indices) > 0:
        best_fp = fp_indices[np.argmax(y_probs[fp_indices])]
        cases.append(build_case_dict(best_fp, "False Positive (Type I Error)"))

    # 4. False Negative (if present)
    if len(fn_indices) > 0:
        best_fn = fn_indices[np.argmin(y_probs[fn_indices])]
        cases.append(build_case_dict(best_fn, "False Negative (Type II Error)"))

    return cases
