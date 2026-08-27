from pydantic import BaseModel

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