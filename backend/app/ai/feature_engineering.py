"""
MediShield AI: Domain Feature Engineering Module
Module: backend.app.ai.feature_engineering

Implements 5 domain-informed supply-chain features with numerical epsilon protection.
Target-free transformations ensuring zero target leakage.
"""

from typing import List, Union
import numpy as np
import pandas as pd

EPSILON = 1e-5

RAW_FEATURE_COLUMNS = [
    "inventory",
    "demand",
    "lead_time",
    "supplier_reliability",
    "expiry_days",
    "safety_stock",
]

ENGINEERED_FEATURE_COLUMNS = [
    "stock_cover_ratio",
    "safety_buffer_margin",
    "lead_time_demand",
    "reorder_deficit",
    "supplier_delay_exposure",
]

ALL_FEATURE_COLUMNS = RAW_FEATURE_COLUMNS + ENGINEERED_FEATURE_COLUMNS


def compute_domain_features(df: Union[pd.DataFrame, dict]) -> pd.DataFrame:
    """
    Computes domain features for a DataFrame or single observation dictionary.
    
    Features:
    1. Stock Cover Ratio: inventory / (demand + eps)
       Measures how many months of stock are available based on current demand.
    2. Safety Buffer Margin: (inventory - safety_stock) / (demand + eps)
       Measures the surplus or deficit relative to required safety stock normalized by demand.
    3. Lead Time Demand: (demand / 30) * lead_time
       Expected drug consumption during supplier replenishment window.
    4. Reorder Deficit: ((demand / 30) * lead_time + safety_stock) - inventory
       Immediate unit deficit relative to the classical reorder point.
    5. Supplier Delay Exposure: (100 - supplier_reliability) * lead_time
       Quantifies vulnerability to shipment delays based on supplier historical failure rate.
    """
    if isinstance(df, dict):
        df_in = pd.DataFrame([df])
    else:
        df_in = df.copy()

    # Verify required raw features
    for col in RAW_FEATURE_COLUMNS:
        if col not in df_in.columns:
            raise ValueError(f"Missing required raw feature column: '{col}'")

    inv = df_in["inventory"].astype(float)
    dem = df_in["demand"].astype(float)
    lt = df_in["lead_time"].astype(float)
    sr = df_in["supplier_reliability"].astype(float)
    ss = df_in["safety_stock"].astype(float)

    # 1. Stock Cover Ratio
    df_in["stock_cover_ratio"] = inv / (dem + EPSILON)

    # 2. Safety Buffer Margin
    df_in["safety_buffer_margin"] = (inv - ss) / (dem + EPSILON)

    # 3. Lead Time Demand
    df_in["lead_time_demand"] = (dem / 30.0) * lt

    # 4. Reorder Deficit
    df_in["reorder_deficit"] = ((dem / 30.0) * lt + ss) - inv

    # 5. Supplier Delay Exposure
    df_in["supplier_delay_exposure"] = (100.0 - sr) * lt

    return df_in


def get_feature_metadata():
    """Returns documentation and mathematical formulation for each engineered feature."""
    return [
        {
            "name": "stock_cover_ratio",
            "formula": "inventory / (demand + epsilon)",
            "unit": "months of supply",
            "description": "Stock autonomy relative to monthly consumption rate.",
            "expected_risk_relationship": "Negative: higher stock cover lowers shortage risk.",
        },
        {
            "name": "safety_buffer_margin",
            "formula": "(inventory - safety_stock) / (demand + epsilon)",
            "unit": "ratio",
            "description": "Inventory buffer remaining above designated safety threshold.",
            "expected_risk_relationship": "Negative: higher safety margin lowers shortage risk.",
        },
        {
            "name": "lead_time_demand",
            "formula": "(demand / 30) * lead_time",
            "unit": "units",
            "description": "Expected units consumed while waiting for order replenishment.",
            "expected_risk_relationship": "Positive: higher consumption during lead time increases vulnerability.",
        },
        {
            "name": "reorder_deficit",
            "formula": "((demand / 30) * lead_time + safety_stock) - inventory",
            "unit": "units",
            "description": "Deficit between required reorder inventory and actual current inventory.",
            "expected_risk_relationship": "Positive: positive deficit indicates immediate need to reorder.",
        },
        {
            "name": "supplier_delay_exposure",
            "formula": "(100 - supplier_reliability) * lead_time",
            "unit": "risk days",
            "description": "Interaction between supplier delivery risk and lead time.",
            "expected_risk_relationship": "Positive: higher delay exposure increases stockout hazard.",
        },
    ]
