from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Supplier

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

# Weight values from research paper
W1 = 0.35   # Reliability
W2 = 0.30   # Quality
W3 = 0.20   # Cost
W4 = 0.15   # Delivery

@router.get("/")
def get_suppliers(db: Session = Depends(get_db)):

    suppliers = db.query(Supplier).all()
    results = []

    for s in suppliers:

        # Lower cost & delivery time = higher score
        cost_score = 150 - s.cost
        delivery_score = 10 - s.delivery_days

        score = (
            W1 * s.reliability +
            W2 * s.quality_score +
            W3 * cost_score +
            W4 * delivery_score * 10
        )

        s.score = round(score, 2)

        results.append({
            "id": s.id,
            "name": s.name,
            "quality": s.quality_score,
            "reliability": s.reliability,
            "delivery": s.delivery_days,
            "cost": s.cost,
            "score": round(score, 2)
        })

    db.commit()

    results.sort(key=lambda x: x["score"], reverse=True)

    return results


@router.get("/best")
def best_supplier(db: Session = Depends(get_db)):

    suppliers = get_suppliers(db)

    return suppliers[0]