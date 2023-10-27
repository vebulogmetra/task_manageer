from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    due_date: str
    user_id: UUID
    project_id: UUID


class TaskCreate(Task):
    pass


class TaskGet(Task):
    id: UUID
    created_at: str
    updated_at: str


class TaskComment(BaseModel):
    content: str
    user_id: UUID
    task_id: UUID


class TaskCommentCreate(TaskComment):
    pass


class TaskCommentGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: str
