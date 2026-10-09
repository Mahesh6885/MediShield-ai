"""
MediShield AI: Direction-Aware Multi-Criteria Supplier Ranking & Sensitivity Analysis
Module: backend.app.ai.supplier_ranking

Implements direction-aware min-max normalization:
- Benefit criteria (higher = better): reliability, quality
- Cost criteria (lower = better): procurement cost, delivery days

Includes weight sensitivity analysis (+/- 20% perturbation with renormalization).
"""

import os
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr


# Predefined experimental baseline weights (documented as research baseline, not claimed as expert elicitation)
BASELINE_WEIGHTS = {
    "reliability": 0.35,  # Benefit
    "quality": 0.30,      # Benefit
    "cost": 0.20,         # Cost (lower is better)
    "delivery": 0.15,     # Cost (lower is better)
}


def normalize_series(values: np.ndarray, criterion_type: str = "benefit") -> np.ndarray:
    """
    Direction-aware min-max normalization.
    
    benefit: (x - min) / (max - min)
    cost:    (max - x) / (max - min)
    Safely handles min == max edge case by returning 1.0.
    """
    v_min = np.min(values)
    v_max = np.max(values)
    diff = v_max - v_min

    if np.isclose(diff, 0.0):
        return np.ones_like(values, dtype=float)

    if criterion_type == "benefit":
        return (values - v_min) / diff
    elif criterion_type == "cost":
        return (v_max - values) / diff
    else:
        raise ValueError(f"Unknown criterion type '{criterion_type}'. Must be 'benefit' or 'cost'.")


def compute_supplier_scores(
    suppliers: List[Dict[str, Any]],
    weights: Dict[str, float] = None,
) -> Tuple[List[Dict[str, Any]], pd.DataFrame]:
    """
    Computes direction-aware normalized multi-criteria scores for suppliers.
    
    Args:
        suppliers: list of dicts with keys 'id', 'name', 'reliability', 'quality', 'cost', 'delivery'
        weights: dict of weights for each criterion (must sum to ~1.0)
    """
    if weights is None:
        weights = BASELINE_WEIGHTS.copy()

    # Normalize weights so they sum strictly to 1.0
    w_sum = sum(weights.values())
    norm_w = {k: v / w_sum for k, v in weights.items()}

    df = pd.DataFrame(suppliers)
    
    # Extract numerical arrays
    rel = df["reliability"].astype(float).values
    qua = df["quality"].astype(float).values
    cst = df["cost"].astype(float).values
    deliv = df["delivery"].astype(float).values

    # Direction-aware normalization
    norm_rel = normalize_series(rel, "benefit")
    norm_qua = normalize_series(qua, "benefit")
    norm_cst = normalize_series(cst, "cost")
    norm_deliv = normalize_series(deliv, "cost")

    df["norm_reliability"] = np.round(norm_rel, 4)
    df["norm_quality"] = np.round(norm_qua, 4)
    df["norm_cost"] = np.round(norm_cst, 4)
    df["norm_delivery"] = np.round(norm_deliv, 4)

    # Composite score: mapped to 0-100 scale for intuitive display
    composite_score_0_1 = (
        norm_w["reliability"] * norm_rel
        + norm_w["quality"] * norm_qua
        + norm_w["cost"] * norm_cst
        + norm_w["delivery"] * norm_deliv
    )
    df["composite_score"] = np.round(composite_score_0_1 * 100.0, 2)
    df["rank"] = df["composite_score"].rank(ascending=False, method="min").astype(int)

    df_sorted = df.sort_values(by="composite_score", ascending=False).reset_index(drop=True)

    results = df_sorted.to_dict(orient="records")
    return results, df_sorted


def run_weight_sensitivity_analysis(
    suppliers: List[Dict[str, Any]],
    perturbation_pct: float = 0.20,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Evaluates ranking stability by perturbing each criterion weight by +/- 20%
    and renormalizing the remaining weights so the sum remains 1.0.
    """
    _, df_nominal = compute_supplier_scores(suppliers, BASELINE_WEIGHTS)
    nominal_ranking = df_nominal.set_index("name")["rank"].to_dict()

    scenarios = [{"scenario": "Nominal", "perturbed_criterion": "None", "perturbation": "0%", **BASELINE_WEIGHTS}]

    for crit in BASELINE_WEIGHTS:
        for factor, label in [(1.0 - perturbation_pct, f"-{int(perturbation_pct*100)}%"),
                              (1.0 + perturbation_pct, f"+{int(perturbation_pct*100)}%")]:
            perturbed = BASELINE_WEIGHTS.copy()
            perturbed[crit] *= factor
            
            # Renormalize other weights
            other_sum = sum(v for k, v in BASELINE_WEIGHTS.items() if k != crit)
            target_other_sum = 1.0 - perturbed[crit]
            for k in perturbed:
                if k != crit:
                    perturbed[k] = (perturbed[k] / other_sum) * target_other_sum

            scenarios.append({
                "scenario": f"{crit}_{label}",
                "perturbed_criterion": crit,
                "perturbation": label,
                **perturbed
            })

    results_rows = []
    kendall_taus = []
    spearman_rhos = []

    for sc in scenarios:
        weights = {k: sc[k] for k in BASELINE_WEIGHTS}
        _, df_sc = compute_supplier_scores(suppliers, weights)
        sc_ranking = df_sc.set_index("name")["rank"].to_dict()

        # Compute rank correlations vs nominal
        nom_ranks = [nominal_ranking[n] for n in df_nominal["name"]]
        pert_ranks = [sc_ranking[n] for n in df_nominal["name"]]
        
        tau, _ = kendalltau(nom_ranks, pert_ranks)
        rho, _ = spearmanr(nom_ranks, pert_ranks)
        
        kendall_taus.append(tau if not np.isnan(tau) else 1.0)
        spearman_rhos.append(rho if not np.isnan(rho) else 1.0)

        row = {
            "scenario": sc["scenario"],
            "criterion": sc["perturbed_criterion"],
            "delta": sc["perturbation"],
            "top_supplier": df_sc.iloc[0]["name"],
            "top_score": df_sc.iloc[0]["composite_score"],
            "kendall_tau": round(tau, 4) if not np.isnan(tau) else 1.0,
            "spearman_rho": round(rho, 4) if not np.isnan(rho) else 1.0,
        }
        for n in df_nominal["name"]:
            row[f"rank_{n}"] = sc_ranking[n]
        results_rows.append(row)

    df_sens = pd.DataFrame(results_rows)

    summary = {
        "num_scenarios": len(scenarios),
        "scenarios_description": "9 deterministic single-criterion +/-20% perturbation bounds",
        "mean_kendall_tau": round(float(np.mean(kendall_taus)), 4),
        "min_kendall_tau": round(float(np.min(kendall_taus)), 4),
        "mean_spearman_rho": round(float(np.mean(spearman_rhos)), 4),
        "top_supplier_nominal": df_nominal.iloc[0]["name"],
        "top_supplier_stability_rate": round(
            float(sum(1 for r in results_rows if r["top_supplier"] == df_nominal.iloc[0]["name"]) / len(results_rows) * 100), 2
        ),
    }

    return df_sens, summary


def run_monte_carlo_sensitivity_trials(
    suppliers: List[Dict[str, Any]],
    num_trials: int = 200,
    perturbation_pct: float = 0.20,
    seed: int = 42,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Executes 200 random perturbation trials across all criteria simultaneously.
    Each weight w_i is perturbed by uniform delta in [-perturbation_pct, +perturbation_pct],
    renormalized to sum to 1.0, and evaluated for rank stability vs nominal.
    """
    rng = np.random.RandomState(seed)
    _, df_nominal = compute_supplier_scores(suppliers, BASELINE_WEIGHTS)
    nominal_ranking = df_nominal.set_index("name")["rank"].to_dict()
    nom_ranks = [nominal_ranking[n] for n in df_nominal["name"]]

    crit_keys = list(BASELINE_WEIGHTS.keys())
    base_w_arr = np.array([BASELINE_WEIGHTS[k] for k in crit_keys])

    trials_data = []
    kendall_taus = []
    spearman_rhos = []
    top_suppliers = []

    for trial_idx in range(1, num_trials + 1):
        # Sample multiplicative perturbation factors in [1 - perturbation_pct, 1 + perturbation_pct]
        factors = 1.0 + rng.uniform(-perturbation_pct, perturbation_pct, size=len(crit_keys))
        raw_perturbed = base_w_arr * factors
        norm_weights = raw_perturbed / np.sum(raw_perturbed)

        trial_weight_dict = {k: float(norm_weights[i]) for i, k in enumerate(crit_keys)}
        _, df_trial = compute_supplier_scores(suppliers, trial_weight_dict)
        trial_ranking = df_trial.set_index("name")["rank"].to_dict()
        trial_scores = df_trial.set_index("name")["composite_score"].to_dict()

        pert_ranks = [trial_ranking[n] for n in df_nominal["name"]]
        tau, _ = kendalltau(nom_ranks, pert_ranks)
        rho, _ = spearmanr(nom_ranks, pert_ranks)

        t_val = tau if not np.isnan(tau) else 1.0
        r_val = rho if not np.isnan(rho) else 1.0
        kendall_taus.append(t_val)
        spearman_rhos.append(r_val)

        top_sup = df_trial.iloc[0]["name"]
        top_suppliers.append(top_sup)

        trials_data.append({
            "trial": trial_idx,
            "perturbed_weights": {k: round(float(raw_perturbed[i]), 4) for i, k in enumerate(crit_keys)},
            "normalized_weights": {k: round(float(norm_weights[i]), 4) for i, k in enumerate(crit_keys)},
            "supplier_scores": {k: round(float(v), 2) for k, v in trial_scores.items()},
            "rankings": trial_ranking,
            "top_supplier": top_sup,
            "kendall_tau": round(float(t_val), 4),
            "spearman_rho": round(float(r_val), 4),
        })

    df_trials = pd.DataFrame(trials_data)

    mc_summary = {
        "num_trials": num_trials,
        "perturbation_range": f"+/- {int(perturbation_pct * 100)}%",
        "random_seed": seed,
        "top_supplier_nominal": df_nominal.iloc[0]["name"],
        "top_supplier_stability_rate_pct": round(
            float(sum(1 for s in top_suppliers if s == df_nominal.iloc[0]["name"]) / num_trials * 100.0), 2
        ),
        "mean_kendall_tau": round(float(np.mean(kendall_taus)), 4),
        "std_kendall_tau": round(float(np.std(kendall_taus)), 4),
        "min_kendall_tau": round(float(np.min(kendall_taus)), 4),
        "mean_spearman_rho": round(float(np.mean(spearman_rhos)), 4),
        "std_spearman_rho": round(float(np.std(spearman_rhos)), 4),
    }

    return df_trials, mc_summary

