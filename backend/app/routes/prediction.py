from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import Medicine, PredictionHistory
from ..ai.predict import predict_shortage

router = APIRouter(prefix="/prediction", tags=["Prediction"])

@router.get("/history")
def history(db: Session = Depends(get_db)):
    return db.query(PredictionHistory).order_by(
        PredictionHistory.id.desc()
    ).limit(20).all()
@router.post("/{medicine_id}")
def predict(medicine_id: int, db: Session = Depends(get_db)):

    med = db.query(Medicine).filter(Medicine.id == medicine_id).first()

    expiry_days = (
        datetime.strptime(med.expiry_date, "%Y-%m-%d") -
        datetime.today()
    ).days

    features = {
        "inventory": med.inventory,
        "demand": med.demand,
        "lead_time": med.lead_time,
        "supplier_reliability": med.supplier_reliability,
        "expiry_days": expiry_days,
        "safety_stock": med.safety_stock
    }

    result = predict_shortage(features)

    med.shortage_probability = result["probability"]
    med.risk_level = result["risk"]

    history = PredictionHistory(
        medicine_name=med.name,
        probability=result["probability"],
        risk_level=result["risk"],
        shap_reason=result["explanation"][0]["feature"],
        predicted_at=str(datetime.now())
    )

    db.add(history)
    db.commit()

    return result