from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import Medicine

router = APIRouter(prefix="/inventory", tags=["Inventory"])

ORDERING_COST = 200
HOLDING_COST = 15

@router.get("/")
def inventory_dashboard(db: Session = Depends(get_db)):

    medicines = db.query(Medicine).all()

    inventory_list = []

    for med in medicines:

        expiry_days = (
            datetime.strptime(med.expiry_date,"%Y-%m-%d")
            - datetime.today()
        ).days

        daily_demand = med.demand / 30

        reorder_point = int(
            daily_demand * med.lead_time + med.safety_stock
        )

        annual_demand = med.demand * 12

        eoq = int(((2 * annual_demand * ORDERING_COST)/HOLDING_COST)**0.5)

        med.reorder_point = reorder_point
        med.eoq = eoq

        inventory_list.append({
            "id": med.id,
            "name": med.name,
            "inventory": med.inventory,
            "demand": med.demand,
            "safety_stock": med.safety_stock,
            "reorder_point": reorder_point,
            "eoq": eoq,
            "expiry_days": expiry_days,
            "status": (
                "LOW STOCK"
                if med.inventory <= med.safety_stock
                else "REORDER"
                if med.inventory <= reorder_point
                else "HEALTHY"
            )
        })

    db.commit()

    return inventory_list