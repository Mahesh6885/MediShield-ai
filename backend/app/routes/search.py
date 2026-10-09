from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Medicine

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
def search(query: str, db: Session = Depends(get_db)):
    medicines = (
        db.query(Medicine)
        .filter(Medicine.name.ilike(f"%{query}%"))
        .limit(10)
        .all()
    )

    return medicines