from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routes import registration


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def home():
    return {"message": "AI Workflow Platform API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(registration.router)


