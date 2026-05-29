from sqlmodel import Session, select
from fastapi import HTTPException

from app.database import engine
from app.models import Task

# -----------------------------
# Create Task
# -----------------------------
def create_task(task: Task):

    with Session(engine) as session:

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

# -----------------------------
# Get All Tasks
# -----------------------------
def get_all_tasks():

    with Session(engine) as session:

        tasks = session.exec(select(Task)).all()

        return tasks

# -----------------------------
# Get Single Task
# -----------------------------
def get_task(task_id: int):

    with Session(engine) as session:

        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return task

# -----------------------------
# Update Task
# -----------------------------
def update_task(task_id: int, updated_task: Task):

    with Session(engine) as session:

        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        task.title = updated_task.title
        task.priority = updated_task.priority
        task.department = updated_task.department

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

# -----------------------------
# Delete Task
# -----------------------------
def delete_task(task_id: int):

    with Session(engine) as session:

        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        session.delete(task)
        session.commit()

        return {
            "message": "Task deleted successfully"
        }
