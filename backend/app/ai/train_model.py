"""
MediShield AI: XGBoost Shortage Classifier Training Pipeline
Module: backend.app.ai.train_model

Trains the production XGBoost classifier on the corrected synthetic dataset with
domain-engineered supply chain features.
"""

import os
import sys
import joblib
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# Support both package imports and standalone script execution
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
backend_dir = os.path.dirname(app_dir)
root_dir = os.path.dirname(backend_dir)
for p in [current_dir, app_dir, backend_dir, root_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from .data_generation import generate_synthetic_dataset
    from .feature_engineering import compute_domain_features, ALL_FEATURE_COLUMNS, RAW_FEATURE_COLUMNS
except ImportError:
    from data_generation import generate_synthetic_dataset
    from feature_engineering import compute_domain_features, ALL_FEATURE_COLUMNS, RAW_FEATURE_COLUMNS


MODEL_PATH = os.path.join(current_dir, "xgboost_model.pkl")


def train_production_model(save_path: str = MODEL_PATH):
    print("Generating training dataset with corrected domain formulation (safety_stock = -2.0)...")
    df_raw, meta = generate_synthetic_dataset(num_samples=5000, seed=42)

    print("Computing domain engineered features...")
    df_feat = compute_domain_features(df_raw)

    X = df_feat[ALL_FEATURE_COLUMNS]
    y = df_feat["shortage"]

    # Stratified 80/20 train/test split to evaluate generalization
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print("Training XGBoost Classifier...")
    model = XGBClassifier(
        n_estimators=150,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss",
    )
    model.fit(X_train, y_train)

    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    print(f"Model trained. Train Accuracy: {train_acc*100:.2f}%, Test Accuracy: {test_acc*100:.2f}%")

    model_artifact = {
        "model": model,
        "feature_names": ALL_FEATURE_COLUMNS,
        "raw_features": RAW_FEATURE_COLUMNS,
        "train_accuracy": train_acc,
        "test_accuracy": test_acc,
    }

    joblib.dump(model_artifact, save_path)
    print(f"Model artifact successfully saved to: {save_path}")
    return model_artifact


if __name__ == "__main__":
    train_production_model()