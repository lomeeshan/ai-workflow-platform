from sqlmodel import Session

from app.schemas import TaskCreate
from app.services.llm_service import analyze_task_with_llm
from app import crud


def create_ai_analyzed_task(db: Session, task_data: TaskCreate):
    analysis = analyze_task_with_llm(
        title=task_data.title,
        description=task_data.description,
    )

    saved_task = crud.create_task(
        db=db,
        task_data=task_data,
        analysis=analysis,
    )

    return saved_task


def reanalyze_existing_task(db: Session, task_id: int):
    task = crud.get_task_by_id(db=db, task_id=task_id)

    if not task:
        return None

    analysis = analyze_task_with_llm(
        title=task.title,
        description=task.description,
    )

    updated_task = crud.update_task_analysis(
        db=db,
        task_id=task_id,
        analysis=analysis,
    )

    return updated_task
