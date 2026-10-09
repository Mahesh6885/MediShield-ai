from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("/")
def get_settings(db: Session = Depends(get_db)):
    return crud.get_settings(db)


@router.put("/")
def save_settings(
    data: schemas.SettingUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_settings(db, data)