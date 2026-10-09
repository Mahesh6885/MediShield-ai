"""
MediShield AI: Clinical & Decision Support Assistant Router
Module: backend.app.routes.assistant

Connects to the true RAG pipeline (document ingestion, vector embeddings, top-k retrieval,
grounded evidence synthesis, and SQLite context augmentation).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..ai.rag.pipeline import get_rag_pipeline

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    user: str
    assistant: str
    citations: Optional[List[Dict[str, Any]]] = None
    latency_ms: Optional[float] = None
    grounded: Optional[bool] = None


@router.post("/chat")
def chat(data: ChatMessage, db: Session = Depends(get_db)):
    pipeline = get_rag_pipeline()
    result = pipeline.query(question=data.message, top_k=3, db=db)

    return {
        "user": data.message,
        "assistant": result["answer"],
        "citations": result["citations"],
        "latency_ms": result["latency_ms"],
        "grounded": result["grounded"],
    }