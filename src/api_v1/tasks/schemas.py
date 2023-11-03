from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.api_v1.associates.schemas import WithUser


class TaskComment(BaseModel):
    content: str
    user_id: UUID
    task_id: UUID


class TaskCommentCreate(TaskComment):
    ...


class TaskCommentUpdate(TaskComment):
    ...


class TaskCommentGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    content: str
    created_at: datetime


class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime
    creator_id: UUID
    project_id: UUID


class TaskCreate(Task):
    due_date: datetime = datetime.now()


class TaskGet(Task):
    id: UUID
    users: Optional[list[WithUser]]
    comments: Optional[list[TaskCommentGet]]
    created_at: datetime
    updated_at: datetime


class TaskUpdate(Task):
    ...
