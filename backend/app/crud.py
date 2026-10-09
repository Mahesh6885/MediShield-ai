from sqlalchemy.orm import Session
from . import models, schemas
from .models import User, Notification, Setting

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

# ---------------- PROFILE ----------------

def get_user(db):
    return db.query(User).first()


def update_user(db, data):
    user = db.query(User).first()

    user.full_name = data.full_name
    user.email = data.email
    user.phone = data.phone
    user.department = data.department
    user.hospital = data.hospital

    db.commit()
    db.refresh(user)

    return user


def change_password(db, current_password, new_password):
    user = db.query(User).first()

    if user.password != current_password:
        return False

    user.password = new_password
    db.commit()

    return True


# ---------------- NOTIFICATIONS ----------------

def get_notifications(db):
    return db.query(Notification).order_by(Notification.created_at.desc()).all()


def mark_notification_read(db, notification_id):
    note = db.query(Notification).filter(Notification.id == notification_id).first()

    if note:
        note.is_read = True
        db.commit()

    return note


def mark_all_notifications(db):
    db.query(Notification).update({"is_read": True})
    db.commit()


def delete_notification(db, notification_id):
    note = db.query(Notification).filter(Notification.id == notification_id).first()

    if note:
        db.delete(note)
        db.commit()


# ---------------- SETTINGS ----------------

def get_settings(db):
    return db.query(Setting).first()


def update_settings(db, data):
    setting = db.query(Setting).first()

    setting.theme = data.theme
    setting.email_alert = data.email_alert
    setting.sms_alert = data.sms_alert
    setting.desktop_alert = data.desktop_alert

    db.commit()
    db.refresh(setting)

    return setting