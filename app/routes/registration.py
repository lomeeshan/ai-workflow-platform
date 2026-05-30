from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas import TaskCreate, TaskUpdate, TaskRead
from app.services.workflow_service import create_ai_analyzed_task
from app import crud


router = APIRouter()


@router.post("/tasks", response_model=TaskRead)
def create_task(task_data: TaskCreate, db: Session = Depends(get_session)):
    try:
        task = create_ai_analyzed_task(db=db, task_data=task_data)
        return task

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks", response_model=list[TaskRead])
def read_tasks(db: Session = Depends(get_session)):
    return crud.get_tasks(db)


@router.get("/tasks/filter/", response_model=list[TaskRead])
def filter_tasks(
    category: Optional[str] = None,
    priority: Optional[str] = None,
    estimated_effort: Optional[str] = None,
    db: Session = Depends(get_session),
):
    return crud.filter_tasks(
        db=db,
        category=category,
        priority=priority,
        estimated_effort=estimated_effort,
    )


@router.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(task_id: int, db: Session = Depends(get_session)):
    task = crud.get_task_by_id(db=db, task_id=task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_session),
):
    updated_task = crud.update_task(
        db=db,
        task_id=task_id,
        task_update=task_update,
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_session)):
    deleted_task = crud.delete_task(db=db, task_id=task_id)

    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "message": "Task deleted successfully",
        "deleted_task_id": task_id,
    }
