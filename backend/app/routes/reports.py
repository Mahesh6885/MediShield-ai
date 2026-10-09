from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Medicine

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/")
def get_reports(db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()

    report = []

    for m in medicines:
        report.append({
            "id": m.id,
            "name": m.name,
            "inventory": m.inventory,
            "risk": m.risk_level if m.risk_level else "Low",
            "expiry": str(m.expiry_date)
        })

    return report