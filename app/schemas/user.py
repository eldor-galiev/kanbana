from typing import Optional

from pydantic import BaseModel


# Базовая схема для чтения и общая схема для других наследников
class UserBase(BaseModel):
    name: str
    email: str

# Схема для создания нового пользователя
class UserCreate(UserBase):
    pass

# Схема для чтения данных пользователя (например, при GET запросах)
class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True  # Это необходимо для работы с SQLAlchemy объектами

# Схема для обновления пользователя (возможность обновить только часть полей)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
