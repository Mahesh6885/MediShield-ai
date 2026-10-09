"""
MediShield AI: Reproducible Synthetic Data Generation Pipeline
Module: backend.app.ai.data_generation

Generates a synthetic medicine-shortage dataset using a domain-informed supply-chain
risk formulation with the corrected protective safety-stock sign.

Source Description:
"Synthetic medicine-shortage dataset generated using a domain-informed supply-chain risk formulation."
"""

import os
import json
import random
from datetime import datetime, timezone
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


# Default generative constants preserving original domain formulation
DEFAULT_SEED = 42
DEFAULT_NUM_SAMPLES = 5000

# Feature sampling boundaries (discrete uniform distributions)
SAMPLING_SPECS = {
    "inventory": {"low": 5, "high": 200, "unit": "units", "desc": "Current physical stock on hand"},
    "demand": {"low": 20, "high": 220, "unit": "units/month", "desc": "Monthly forecasted demand"},
    "lead_time": {"low": 1, "high": 8, "unit": "days", "desc": "Replenishment lead time in days"},
    "supplier_reliability": {"low": 60, "high": 99, "unit": "%", "desc": "Supplier historical fulfillment rate"},
    "expiry_days": {"low": 15, "high": 365, "unit": "days", "desc": "Days remaining until product expiration"},
    "safety_stock": {"low": 5, "high": 25, "unit": "units", "desc": "Designated safety buffer stock"},
}

# Formulation coefficients:
# Notice: Safety stock is protective against stockout risk, hence coefficient is -2.0.
# The original flawed implementation used +2.0, causing an inverted relationship.
FORMULATION_WEIGHTS = {
    "demand": 0.45,
    "inventory": -0.35,
    "lead_time": 8.0,
    "supplier_reliability": -0.30,
    "expiry_days": -0.05,
    "safety_stock": -2.0,  # Corrected: Protective contribution
}

# The threshold of -20.0 preserves the original risk baseline adjusted for the sign change:
# E[SS] = 15; change from +2.0*15 (+30) to -2.0*15 (-30) causes a -60 shift in mean score.
# Original threshold: 40.0 -> Corrected threshold: 40.0 - 60.0 = -20.0.
DEFAULT_THRESHOLD = -20.0


def compute_risk_score(
    inventory: float,
    demand: float,
    lead_time: float,
    supplier_reliability: float,
    expiry_days: float,
    safety_stock: float,
    ss_coeff: float = -2.0,
) -> float:
    """Computes continuous risk score using the domain-informed linear formulation."""
    return (
        demand * FORMULATION_WEIGHTS["demand"]
        + inventory * FORMULATION_WEIGHTS["inventory"]
        + lead_time * FORMULATION_WEIGHTS["lead_time"]
        + supplier_reliability * FORMULATION_WEIGHTS["supplier_reliability"]
        + expiry_days * FORMULATION_WEIGHTS["expiry_days"]
        + safety_stock * ss_coeff
    )


def generate_synthetic_dataset(
    num_samples: int = DEFAULT_NUM_SAMPLES,
    seed: int = DEFAULT_SEED,
    threshold: float = DEFAULT_THRESHOLD,
    ss_coeff: float = -2.0,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Generates synthetic medicine shortage observations reproducibly.
    
    Returns:
        df: pandas DataFrame containing raw features, raw_score, and binary shortage label.
        metadata: dictionary of generation provenance and parameter configuration.
    """
    rng = random.Random(seed)
    rows = []

    for _ in range(num_samples):
        inv = rng.randint(SAMPLING_SPECS["inventory"]["low"], SAMPLING_SPECS["inventory"]["high"])
        dem = rng.randint(SAMPLING_SPECS["demand"]["low"], SAMPLING_SPECS["demand"]["high"])
        lt = rng.randint(SAMPLING_SPECS["lead_time"]["low"], SAMPLING_SPECS["lead_time"]["high"])
        sr = rng.randint(SAMPLING_SPECS["supplier_reliability"]["low"], SAMPLING_SPECS["supplier_reliability"]["high"])
        exp = rng.randint(SAMPLING_SPECS["expiry_days"]["low"], SAMPLING_SPECS["expiry_days"]["high"])
        ss = rng.randint(SAMPLING_SPECS["safety_stock"]["low"], SAMPLING_SPECS["safety_stock"]["high"])

        score = compute_risk_score(
            inventory=inv,
            demand=dem,
            lead_time=lt,
            supplier_reliability=sr,
            expiry_days=exp,
            safety_stock=ss,
            ss_coeff=ss_coeff,
        )
        shortage = 1 if score > threshold else 0

        rows.append({
            "inventory": inv,
            "demand": dem,
            "lead_time": lt,
            "supplier_reliability": sr,
            "expiry_days": exp,
            "safety_stock": ss,
            "raw_score": round(score, 4),
            "shortage": shortage,
        })

    df = pd.DataFrame(rows)

    total_records = len(df)
    shortage_count = int(df["shortage"].sum())
    no_shortage_count = total_records - shortage_count

    metadata = {
        "source": "Synthetic medicine-shortage dataset generated using a domain-informed supply-chain risk formulation.",
        "scientific_integrity_notice": "Synthetically generated benchmark dataset. Not derived from clinical hospital EHR or confidential pharmaceutical firm databases.",
        "generation_method": "Deterministic pseudo-random uniform feature sampling with domain-informed linear composite scoring.",
        "seed": seed,
        "number_of_records": total_records,
        "features": list(SAMPLING_SPECS.keys()),
        "sampling_specifications": SAMPLING_SPECS,
        "label_generation_rule": {
            "formula": (
                "score = 0.45*demand - 0.35*inventory + 8.0*lead_time - 0.30*supplier_reliability "
                "- 0.05*expiry_days - 2.0*safety_stock"
            ),
            "safety_stock_coefficient": ss_coeff,
            "threshold": threshold,
            "decision_rule": f"shortage = 1 if score > {threshold} else 0",
            "domain_correction_rationale": (
                "Safety stock coefficient is negative (-2.0), reflecting its protective buffer role "
                "in mitigating stockout risk."
            ),
        },
        "class_distribution": {
            "no_shortage_0": {
                "count": no_shortage_count,
                "percentage": round(no_shortage_count / total_records * 100, 2),
            },
            "shortage_1": {
                "count": shortage_count,
                "percentage": round(shortage_count / total_records * 100, 2),
            },
        },
        "score_statistics": {
            "mean": round(float(df["raw_score"].mean()), 4),
            "std": round(float(df["raw_score"].std()), 4),
            "min": round(float(df["raw_score"].min()), 4),
            "max": round(float(df["raw_score"].max()), 4),
        },
        "generation_date_utc": datetime.now(timezone.utc).isoformat(),
    }

    return df, metadata


def generate_and_save(
    output_csv_path: str,
    output_meta_path: str,
    num_samples: int = DEFAULT_NUM_SAMPLES,
    seed: int = DEFAULT_SEED,
    threshold: float = DEFAULT_THRESHOLD,
    ss_coeff: float = -2.0,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Generates dataset and writes both CSV and metadata JSON to disk."""
    os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_meta_path)), exist_ok=True)

    df, metadata = generate_synthetic_dataset(
        num_samples=num_samples,
        seed=seed,
        threshold=threshold,
        ss_coeff=ss_coeff,
    )

    df.to_csv(output_csv_path, index=False)
    with open(output_meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return df, metadata


if __name__ == "__main__":
    csv_dest = os.path.join("results", "synthetic_medicine_dataset.csv")
    meta_dest = os.path.join("results", "dataset_metadata.json")
    df_out, meta_out = generate_and_save(csv_dest, meta_dest)
    print(f"Generated {len(df_out)} rows saved to {csv_dest}")
    print(f"Metadata saved to {meta_dest}")
    print(f"Class distribution: {meta_out['class_distribution']}")
