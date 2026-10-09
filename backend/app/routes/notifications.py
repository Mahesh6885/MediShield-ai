from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/")
def get_notifications(db: Session = Depends(get_db)):
    return crud.get_notifications(db)


@router.put("/{notification_id}/read")
def mark_read(notification_id: int, db: Session = Depends(get_db)):
    crud.mark_notification_read(db, notification_id)
    return {"message": "Notification marked as read"}


@router.put("/read-all")
def mark_all(db: Session = Depends(get_db)):
    crud.mark_all_notifications(db)
    return {"message": "All notifications marked as read"}


@router.delete("/{notification_id}")
def delete(notification_id: int, db: Session = Depends(get_db)):
    crud.delete_notification(db, notification_id)
    return {"message": "Notification deleted"}