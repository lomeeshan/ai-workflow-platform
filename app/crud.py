from typing import Optional
from sqlmodel import Session, select

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskAnalysis


def create_task(db: Session, task_data: TaskCreate, analysis: TaskAnalysis) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        category=analysis.category,
        priority=analysis.priority,
        estimated_effort=analysis.estimated_effort,
        ai_summary=analysis.summary,
        ai_reasoning=analysis.reasoning,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(db: Session):
    statement = select(Task)
    results = db.exec(statement).all()
    return results


def get_task_by_id(db: Session, task_id: int):
    return db.get(Task, task_id)


def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    task = db.get(Task, task_id)

    if not task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int):
    task = db.get(Task, task_id)

    if not task:
        return None

    db.delete(task)
    db.commit()

    return task


def filter_tasks(
    db: Session,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    estimated_effort: Optional[str] = None,
):
    statement = select(Task)

    if category:
        statement = statement.where(Task.category == category)

    if priority:
        statement = statement.where(Task.priority == priority)

    if estimated_effort:
        statement = statement.where(Task.estimated_effort == estimated_effort)

    results = db.exec(statement).all()
    return results
