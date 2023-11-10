from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WithUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    username: str
    email: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime


class WithTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime
    creator_id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime


class WithProject(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    creator_id: UUID
    created_at: datetime
    updated_at: datetime


class WithTeam(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    creator_id: UUID
    created_at: datetime
