from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class MedicineBase(BaseModel):
    name: str
    category: str
    inventory: int
    demand: int
    lead_time: int
    supplier: str
    supplier_reliability: int
    expiry_date: str
    safety_stock: int


class MedicineCreate(MedicineBase):
    pass


class MedicineResponse(MedicineBase):
    id: int
    reorder_point: int
    eoq: float
    shortage_probability: float
    risk_level: str

    class Config:
        from_attributes = True
# ================= USER =================

class UserUpdate(BaseModel):
    full_name: str
    email: str
    phone: str
    department: str
    hospital: str

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str


# ================= NOTIFICATION =================

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    priority: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ================= SETTINGS =================

class SettingUpdate(BaseModel):
    theme: str
    email_alert: bool
    sms_alert: bool
    desktop_alert: bool