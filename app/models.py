from typing import Optional
from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # User-provided fields
    title: str
    description: str

    # AI-generated fields
    category: Optional[str] = None
    priority: Optional[str] = None
    estimated_effort: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_reasoning: Optional[str] = None
