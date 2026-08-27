from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..ai.chatbot import chatbot_response

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])

class ChatMessage(BaseModel):
    message:str


@router.post("/chat")
def chat(data:ChatMessage, db:Session=Depends(get_db)):

    answer = chatbot_response(data.message, db)

    return {
        "user": data.message,
        "assistant": answer
    }