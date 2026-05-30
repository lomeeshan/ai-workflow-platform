from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas import TaskCreate, TaskRead
from app.services.workflow_service import create_ai_analyzed_task
from app import crud


router = APIRouter()


@router.post("/tasks", response_model=TaskRead)
def create_task(task_data: TaskCreate, db: Session = Depends(get_session)):
    """
    Create a new task.

    Flow:
    1. Receive title and description from the user.
    2. Send the task to the workflow service.
    3. Workflow service calls Groq.
    4. Groq returns AI analysis.
    5. Task + analysis are saved in PostgreSQL.
    6. Saved task is returned to the client.
    """

    try:
        task = create_ai_analyzed_task(db=db, task_data=task_data)
        return task

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks", response_model=list[TaskRead])
def read_tasks(db: Session = Depends(get_session)):
    """
    Return all stored tasks.
    """

    return crud.get_tasks(db)


@router.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(task_id: int, db: Session = Depends(get_session)):
    """
    Return one task by ID.
    """

    task = crud.get_task_by_id(db=db, task_id=task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
