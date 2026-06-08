from fastapi import FastAPI
from app.routes import tasks


app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Workflow Platform API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(tasks.router)


