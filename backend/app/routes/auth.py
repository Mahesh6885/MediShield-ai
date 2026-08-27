from fastapi import APIRouter
from pydantic import BaseModel

router=APIRouter(prefix="/auth",tags=["Authentication"])

class Login(BaseModel):
    username:str
    password:str

@router.post("/login")
def login(data:Login):

    if data.username=="admin" and data.password=="admin123":
        return {
            "success":True,
            "role":"Admin"
        }

    if data.username=="pharmacist" and data.password=="pharma123":
        return {
            "success":True,
            "role":"Pharmacist"
        }

    return {"success":False}