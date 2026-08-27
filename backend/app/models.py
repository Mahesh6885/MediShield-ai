from sqlalchemy import Column, Integer, Float, String
from .database import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)

    inventory = Column(Integer)
    demand = Column(Integer)
    lead_time = Column(Integer)

    supplier = Column(String)
    supplier_reliability = Column(Integer)

    expiry_date = Column(String)

    safety_stock = Column(Integer)

    reorder_point = Column(Integer, default=0)
    eoq = Column(Float, default=0)

    shortage_probability = Column(Float, default=0)
    risk_level = Column(String, default="Unknown")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    quality_score = Column(Integer)

    reliability = Column(Integer)

    delivery_days = Column(Integer)

    cost = Column(Float)

    score = Column(Float)


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)

    medicine_name = Column(String)

    probability = Column(Float)

    risk_level = Column(String)

    shap_reason = Column(String)

    predicted_at = Column(String)