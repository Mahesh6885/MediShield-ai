from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import medicines, dashboard, prediction, inventory, suppliers, assistant

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediShield AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(medicines.router)
app.include_router(dashboard.router)
app.include_router(prediction.router)
app.include_router(inventory.router)
app.include_router(suppliers.router)
app.include_router(assistant.router)
@app.get("/")
def home():
    return {
        "message": "MediShield AI Backend Running",
        "status": "success"
    }