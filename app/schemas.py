from pydantic import BaseModel

class Task(BaseModel):
    title: str
    priority: str
    department: str
