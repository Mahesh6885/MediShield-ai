from sqlalchemy import Column, Integer, Float, String
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    role = Column(String)
    department = Column(String)
    hospital = Column(String)
    profile_image = Column(String, default="")
    password = Column(String, default="admin123")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(String)
    priority = Column(String)      # Critical / Warning / Info
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String, default="light")
    email_alert = Column(Boolean, default=True)
    sms_alert = Column(Boolean, default=False)
    desktop_alert = Column(Boolean, default=True)
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