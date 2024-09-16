from datetime import datetime, time, timedelta
from select import select

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession



Base = declarative_base()

# Вспомогательная таблица для связи "многие ко многим" между задачами и тегами
task_tags = Table(
    'task_tags', Base.metadata,
    Column('task_id', ForeignKey('tasks.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)


# определяем теги
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Связь "многие ко многим" с задачами
    tasks = relationship('Task', secondary=task_tags, back_populates='tags')


# Определяем модель Task
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)

    tags = relationship('Tag', secondary=task_tags, back_populates='tasks')



    # created_at = Column(DateTime(timezone=True))
    # updated_at = Column(DateTime(timezone=True), onupdate=datetime.now())
    # tags = relationship('Tag', back_populates='notes')





# class Tag(Base):
#     __tablename__ = "tags"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     notes = relationship('Note', back_populates='tags')



async def create_task_with_tags(db: AsyncSession, title: str, description: str, tag_names: list):
    task = Task(title=title, description=description)

    # Поиск тегов или их создание
    for tag_name in tag_names:
        tag = await db.execute(select(Tag).filter(Tag.name == tag_name)).scalar_one_or_none()
        if not tag:
            tag = Tag(name=tag_name)
        task.tags.append(tag)

    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
