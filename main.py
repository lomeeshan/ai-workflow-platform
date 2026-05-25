from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Workflow Platform API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {
                "id": 1,
                "title": "Review client request",
                "priority": "High"
            }
        ]
    }
