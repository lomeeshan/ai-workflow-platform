from fastapi import FastAPI

from app.database import create_db_and_tables
from app.models import Task
from app import crud

app = FastAPI()

# -----------------------------
# Startup Event
# -----------------------------
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# -----------------------------
# Home Route
# -----------------------------
@app.get("/")
def home():
    return {"message": "AI Workflow Platform API is running"}

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# -----------------------------
# Create Task
# -----------------------------
@app.post("/tasks")
def create_task(task: Task):

    created_task = crud.create_task(task)

    return {
        "message": "Task created successfully",
        "task": created_task
    }

# -----------------------------
# Get All Tasks
# -----------------------------
@app.get("/tasks")
def get_tasks():

    tasks = crud.get_all_tasks()

    return {"tasks": tasks}

# -----------------------------
# Get Single Task
# -----------------------------
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    return crud.get_task(task_id)

# -----------------------------
# Update Task
# -----------------------------
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):

    updated = crud.update_task(task_id, updated_task)

    return {
        "message": "Task updated successfully",
        "task": updated
    }

# -----------------------------
# Delete Task
# -----------------------------
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    return crud.delete_task(task_id)


@app.get("/tasks/filter/")
def filter_tasks(priority: str):

    tasks = crud.get_all_tasks()

    filtered_tasks = [
        task for task in tasks
        if task.priority.lower() == priority.lower()
    ]

    return {"tasks": filtered_tasks}


