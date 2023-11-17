from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from src.api_v1.associates.schemas import WithUser


class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime
    creator_id: UUID
    project_id: UUID


class TaskCreate(Task):
    model_config = ConfigDict()
    due_date: datetime = Field(datetime.now())
    creator_id: UUID = Field(None, exclude=True)


class TaskCommentGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    content: str
    created_at: datetime
    user_id: UUID
    task_id: UUID

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        if isinstance(created_at, datetime):
            return created_at.strftime("%d-%m-%Y %H:%M:%S")
        return created_at


class TaskGet(Task):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    users: Optional[list[WithUser]] = []
    comments: Optional[list[TaskCommentGet]] = []
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        if isinstance(created_at, datetime):
            return created_at.strftime("%d-%m-%Y %H:%M:%S")
        return created_at

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime):
        if isinstance(updated_at, datetime):
            return updated_at.strftime("%d-%m-%Y %H:%M:%S")
        return updated_at

    @field_serializer("due_date")
    def serialize_due_date(self, due_date: datetime):
        if isinstance(due_date, datetime):
            return due_date.strftime("%d-%m-%Y")
        return due_date


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskComment(BaseModel):
    content: str
    user_id: UUID
    task_id: UUID


class TaskCommentCreate(TaskComment):
    user_id: Optional[UUID] = None


class TaskCommentUpdate(TaskComment):
    ...


class AddUserToTask(BaseModel):
    task_id: UUID
    user_id: Optional[UUID] = None
