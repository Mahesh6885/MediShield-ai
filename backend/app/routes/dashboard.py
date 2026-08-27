from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import Medicine, Supplier

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def dashboard(db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()
    suppliers = db.query(Supplier).all()

    total = len(medicines)
    low_stock = sum(m.inventory <= m.safety_stock for m in medicines)
    high_risk = sum(m.risk_level == "High" for m in medicines)

    expiring = 0
    for m in medicines:
        days = (
            datetime.strptime(m.expiry_date,"%Y-%m-%d")
            - datetime.today()
        ).days
        if days <= 60:
            expiring += 1

    health = round(((total-low_stock)/(total or 1))*100,2)

    return {
        "total_medicines": total,
        "low_stock": low_stock,
        "high_risk": high_risk,
        "expiring": expiring,
        "suppliers": len(suppliers),
        "inventory_health": health
    }