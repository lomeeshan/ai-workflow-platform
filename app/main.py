from fastapi import FastAPI, HTTPException
from app.schemas import Task

app = FastAPI()

tasks = []

@app.get("/")
def home():
    return {"message": "AI Workflow Platform API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/tasks")
def get_tasks():
    return {"tasks": tasks}

@app.post("/tasks")
def create_task(task: Task):

    tasks.append(task.dict())

    return {
        "message": "Task created successfully",
        "task": task
    }

@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    if task_id >= len(tasks):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return tasks[task_id]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    if task_id >= len(tasks):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = tasks.pop(task_id)

    return {
        "message": "Task deleted successfully",
        "deleted_task": deleted_task
    }
