from pydantic import BaseModel

# Базовая схема задачи
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool | None = None

# Схема для создания задачи
class TaskCreate(TaskBase):
    pass

# Схема для отображения задачи
class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True