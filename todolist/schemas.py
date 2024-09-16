from pydantic import BaseModel
from typing import Optional, List



# Базовая схема задачи
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool | None = None
    # created_at: str | None = None
    # updated_at: str | None = None
    tags: Optional[List[str]] = []  # Список названий тегов (при создании задачи)

# Базовая схема для тегов
class TagBase(BaseModel):
    name: str

# Схема для отображения тегов (с ID)
class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


# Схема для создания задачи
class TaskCreate(TaskBase):
    pass

# Схема для отображения задачи
class Task(TaskBase):
    id: int
    tags: List[Tag]

    class Config:
        orm_mode = True

