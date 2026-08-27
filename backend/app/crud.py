from sqlalchemy.orm import Session
from . import models, schemas

# Get All Medicines
def get_medicines(db: Session):
    return db.query(models.Medicine).all()

# Get Medicine by ID
def get_medicine(db: Session, medicine_id: int):
    return (
        db.query(models.Medicine)
        .filter(models.Medicine.id == medicine_id)
        .first()
    )

# Add Medicine
def create_medicine(db: Session, medicine: schemas.MedicineCreate):
    db_med = models.Medicine(**medicine.model_dump())

    db.add(db_med)
    db.commit()
    db.refresh(db_med)

    return db_med

# Delete Medicine
def delete_medicine(db: Session, medicine_id: int):
    med = get_medicine(db, medicine_id)

    if med:
        db.delete(med)
        db.commit()

    return med