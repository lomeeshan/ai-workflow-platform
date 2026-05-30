from sqlmodel import Session

from app.schemas import TaskCreate
from app.services.llm_service import analyze_task_with_llm
from app import crud


def create_ai_analyzed_task(db: Session, task_data: TaskCreate):
    """
    Coordinates the workflow:
    1. Send task to LLM
    2. Get structured analysis
    3. Save task + analysis to database
    4. Return saved task
    """

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
