"""
MediShield AI: Inventory Optimization Router
Module: backend.app.routes.inventory

Computes dynamic service-level Reorder Point (ROP) and Economic Order Quantity (EOQ):
- Dynamic Safety Stock: SS = z * sigma_d * sqrt(L), with z=1.645 (95% Cycle Service Level)
- Reorder Point: ROP = d * L + SS
- Economic Order Quantity: EOQ = sqrt(2 * D * S / H)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import numpy as np

from ..database import get_db
from ..models import Medicine

router = APIRouter(prefix="/inventory", tags=["Inventory"])

ORDERING_COST = 200.0   # S ($ per order)
HOLDING_COST = 15.0     # H ($ per unit/year)
SERVICE_LEVEL_Z = 1.645 # 95% cycle service level quantile


@router.get("/")
def inventory_dashboard(db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()
    inventory_list = []

    for med in medicines:
        try:
            exp_date = datetime.strptime(med.expiry_date, "%Y-%m-%d")
            expiry_days = (exp_date - datetime.today()).days
        except Exception:
            expiry_days = 90

        daily_demand = max(0.1, med.demand / 30.0)
        # Estimated standard deviation of daily demand assuming Poisson/empirical coefficient of variation ~ 0.5
        sigma_daily_demand = max(0.5, daily_demand * 0.5)
        lead_time = max(1, med.lead_time or 3)

        # Dynamic service-level safety stock calculation
        dynamic_safety_stock = int(np.ceil(SERVICE_LEVEL_Z * sigma_daily_demand * np.sqrt(lead_time)))
        
        # If database safety stock is not populated or smaller, ensure safety buffer meets target service level
        effective_safety_stock = max(med.safety_stock or 0, dynamic_safety_stock)

        reorder_point = int(np.ceil(daily_demand * lead_time + effective_safety_stock))
        annual_demand = med.demand * 12.0
        eoq = int(np.round(((2.0 * annual_demand * ORDERING_COST) / HOLDING_COST) ** 0.5))

        med.reorder_point = reorder_point
        med.eoq = float(eoq)
        med.safety_stock = effective_safety_stock

        status = (
            "LOW STOCK"
            if med.inventory <= effective_safety_stock
            else "REORDER"
            if med.inventory <= reorder_point
            else "HEALTHY"
        )

        inventory_list.append({
            "id": med.id,
            "name": med.name,
            "category": med.category,
            "inventory": med.inventory,
            "demand": med.demand,
            "lead_time": med.lead_time,
            "safety_stock": effective_safety_stock,
            "dynamic_safety_stock": dynamic_safety_stock,
            "reorder_point": reorder_point,
            "eoq": eoq,
            "expiry_days": expiry_days,
            "status": status,
        })

    db.commit()
    return inventory_list