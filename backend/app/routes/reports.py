from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Medicine

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/")
def reports(db:Session=Depends(get_db)):

    meds=db.query(Medicine).all()

    return [
        {
            "name":m.name,
            "inventory":m.inventory,
            "risk":m.risk_level,
            "expiry":m.expiry_date
        }
        for m in meds
    ]