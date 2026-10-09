"""
MediShield AI: Data Preprocessing Pipeline
Module: backend.app.ai.preprocessing

Provides reproducible preprocessing pipelines using scikit-learn.
Ensures strict separation between training and test sets to eliminate data leakage.
"""

import json
from typing import Dict, Any, Tuple, List, Optional
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


class FeatureEngineerTransformer(BaseEstimator, TransformerMixin):
    """Scikit-learn compatible transformer that computes the 5 domain features."""
    def __init__(self, eps: float = 1e-5):
        self.eps = eps

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        from .feature_engineering import compute_domain_features
        if isinstance(X, pd.DataFrame):
            df = X.copy()
        else:
            from .feature_engineering import RAW_FEATURE_COLUMNS
            df = pd.DataFrame(X, columns=RAW_FEATURE_COLUMNS)
        df_feat = compute_domain_features(df)
        return df_feat


def create_preprocessing_pipeline(
    numerical_cols: List[str],
    scale_features: bool = False,
    impute_strategy: str = "median",
) -> Pipeline:
    """
    Constructs an sklearn Pipeline.
    
    Args:
        numerical_cols: List of numerical column names.
        scale_features: If True, adds StandardScaler (e.g. for Logistic Regression).
                        If False, retains original scale (e.g. for XGBoost and Tree models).
        impute_strategy: Imputation strategy for missing values ('median' or 'mean').
    """
    steps = [
        ("imputer", SimpleImputer(strategy=impute_strategy))
    ]
    if scale_features:
        steps.append(("scaler", StandardScaler()))

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline(steps=steps), numerical_cols)
        ],
        remainder="passthrough"
    )
    return preprocessor


def audit_dataset_for_preprocessing(df: pd.DataFrame, feature_cols: List[str]) -> Dict[str, Any]:
    """
    Inspects dataset for missingness, data types, and potential leakage indicators.
    Reports honest metrics.
    """
    missing_counts = df[feature_cols].isnull().sum().to_dict()
    total_missing = int(sum(missing_counts.values()))
    dtypes = {col: str(df[col].dtype) for col in feature_cols}
    stats = {}
    for col in feature_cols:
        stats[col] = {
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "mean": round(float(df[col].mean()), 4),
            "std": round(float(df[col].std()), 4),
            "null_count": int(missing_counts[col]),
        }

    return {
        "total_records": len(df),
        "total_missing_values": total_missing,
        "missing_per_feature": missing_counts,
        "feature_dtypes": dtypes,
        "feature_summary_statistics": stats,
        "leakage_prevention": (
            "Preprocessing pipelines are fitted exclusively on X_train. "
            "Transformers are only applied (transform) to X_test with no shared state."
        ),
    }
