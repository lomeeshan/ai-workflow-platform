from sqlmodel import Session, select

from app.models import Task
from app.schemas import TaskCreate, TaskAnalysis


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
