from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import TaskStatus

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: TaskStatus
    dead_line: Optional[datetime] = None

class TaskCreate(TaskBase):
    project_id: int

class TaskRead(TaskBase):
    id: int
    added_at: datetime

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    dead_line: Optional[datetime] = None
