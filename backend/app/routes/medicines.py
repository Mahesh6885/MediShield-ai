from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..database import get_db
from ..models import Medicine
from ..schemas import MedicineCreate

router = APIRouter(prefix="/medicines", tags=["Medicines"])


@router.get("/")
def get_medicines(
    search: str = "",
    category: str = "",
    db: Session = Depends(get_db)
):
    query = db.query(Medicine)

    if search:
        query = query.filter(
            or_(
                Medicine.name.contains(search),
                Medicine.supplier.contains(search)
            )
        )

    if category:
        query = query.filter(Medicine.category == category)

    return query.all()


@router.post("/")
def add_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    med = Medicine(**medicine.model_dump())
    db.add(med)
    db.commit()
    db.refresh(med)
    return med


@router.put("/{medicine_id}")
def update_medicine(
    medicine_id: int,
    medicine: MedicineCreate,
    db: Session = Depends(get_db)
):
    med = db.query(Medicine).filter(Medicine.id == medicine_id).first()

    for key, value in medicine.model_dump().items():
        setattr(med, key, value)

    db.commit()
    db.refresh(med)
    return med


@router.delete("/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    med = db.query(Medicine).filter(Medicine.id == medicine_id).first()

    db.delete(med)
    db.commit()

    return {"message": "Medicine Deleted"}