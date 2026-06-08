from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


def utc_now():
    return datetime.now(timezone.utc)


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

    # Workflow lifecycle fields
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
