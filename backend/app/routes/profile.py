from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/")
def get_profile(db: Session = Depends(get_db)):
    return crud.get_user(db)


@router.put("/")
def update_profile(
    data: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_user(db, data)


@router.put("/password")
def change_password(
    data: schemas.PasswordUpdate,
    db: Session = Depends(get_db)
):
    ok = crud.change_password(
        db,
        data.current_password,
        data.new_password,
    )

    if not ok:
        raise HTTPException(status_code=400, detail="Wrong current password")

    return {"message": "Password changed successfully"}