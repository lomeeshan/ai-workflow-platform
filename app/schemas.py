from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel


TaskStatus = Literal["pending", "in_progress", "completed", "cancelled"]


class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    estimated_effort: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_reasoning: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    category: Optional[str]
    priority: Optional[str]
    estimated_effort: Optional[str]
    ai_summary: Optional[str]
    ai_reasoning: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime


class TaskAnalysis(BaseModel):
    category: Literal[
        "school",
        "career",
        "personal",
        "finance",
        "health",
        "technical",
        "other",
    ]
    priority: Literal["low", "medium", "high"]
    estimated_effort: Literal["small", "medium", "large"]
    summary: str
    reasoning: str
