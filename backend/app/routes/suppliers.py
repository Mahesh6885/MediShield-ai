"""
MediShield AI: Supplier Recommendation Router
Module: backend.app.routes.suppliers

Computes direction-aware normalized multi-criteria supplier scores:
- Reliability (35%): Benefit (higher is better)
- Quality (30%): Benefit (higher is better)
- Procurement Cost (20%): Cost (lower is better)
- Delivery Lead Time (15%): Cost (lower is better)

Eliminates arbitrary offset constants (150 - cost, 10 - delivery).
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Supplier
from ..ai.supplier_ranking import compute_supplier_scores, BASELINE_WEIGHTS

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.get("/")
def get_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    if not suppliers:
        return []

    # Prepare input payload for multi-criteria engine
    payload = []
    supplier_map = {}
    for s in suppliers:
        supplier_map[s.id] = s
        payload.append({
            "id": s.id,
            "name": s.name,
            "reliability": float(s.reliability),
            "quality": float(s.quality_score),
            "cost": float(s.cost),
            "delivery": float(s.delivery_days),
        })

    # Compute direction-aware normalized scores
    ranked_results, df_ranked = compute_supplier_scores(payload, BASELINE_WEIGHTS)

    # Update database scores and format response
    results = []
    for r in ranked_results:
        s_obj = supplier_map[r["id"]]
        s_obj.score = float(r["composite_score"])
        
        results.append({
            "id": r["id"],
            "name": r["name"],
            "quality": int(r["quality"]),
            "reliability": int(r["reliability"]),
            "delivery": int(r["delivery"]),
            "cost": float(r["cost"]),
            "score": float(r["composite_score"]),
            "rank": int(r["rank"]),
            "norm_reliability": float(r["norm_reliability"]),
            "norm_quality": float(r["norm_quality"]),
            "norm_cost": float(r["norm_cost"]),
            "norm_delivery": float(r["norm_delivery"]),
        })

    db.commit()
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


@router.get("/best")
def best_supplier(db: Session = Depends(get_db)):
    suppliers = get_suppliers(db)
    if not suppliers:
        return {}
    return suppliers[0]