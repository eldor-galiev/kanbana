from datetime import datetime
from typing import List, Optional
from enum import Enum
from sqlalchemy import Enum as SQLEnum

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    projects : Mapped[List['Project']] = relationship('Project', back_populates='owner')

class Project(Base):
    __tablename__ = 'project'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    owner: Mapped['User'] = relationship('User', back_populates='projects')
    tasks: Mapped[List['Task']] = relationship('Task', back_populates='project')


class TaskStatus(str, Enum):
    to_do = 'To do'
    in_progress = 'In progress'
    done = 'Done'


class Task(Base):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.to_do)
    added_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    dead_line: Mapped[Optional[datetime]] = mapped_column(DateTime)

    project: Mapped['Project'] = relationship('Project', back_populates='tasks')