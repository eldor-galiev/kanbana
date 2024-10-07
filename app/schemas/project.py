from pydantic import BaseModel
from typing import List, Optional
from app.schemas.task import TaskRead
# Базовая схема
class ProjectBase(BaseModel):
    name: str

# Схема для создания нового проекта
class ProjectCreate(ProjectBase):
    owner_id: int

# Схема для чтения данных проекта
class ProjectRead(ProjectBase):
    id: int

    class Config:
        from_attributes = True

# Схема для обновления проекта
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
