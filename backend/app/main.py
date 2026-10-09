from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import notifications, profile, settings
from .database import Base, engine
from .routes import medicines, dashboard, prediction, inventory, suppliers, assistant, reports, auth
from app.routes import (
    dashboard,
    medicines,
    inventory,
    suppliers,
    prediction,
    reports,
    assistant,
    profile,
    notifications,
    settings,
    search,
)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediShield AI API")

@app.on_event("startup")
def preload_rag():
    try:
        from .ai.rag.pipeline import get_rag_pipeline
        get_rag_pipeline()
    except Exception as e:
        print(f"Warning: RAG preload failed: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(medicines.router)
app.include_router(inventory.router)
app.include_router(prediction.router)
app.include_router(suppliers.router)
app.include_router(assistant.router)
app.include_router(reports.router)
app.include_router(auth.router)
app.include_router(notifications.router)
app.include_router(profile.router)
app.include_router(settings.router)
app.include_router(search.router)
@app.get("/")
def home():
    return {
        "message": "MediShield AI Backend Running",
        "status": "success"
    }