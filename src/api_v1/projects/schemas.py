from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.api_v1.associates.schemas import WithUser


class Project(BaseModel):
    title: str
    description: str
    creator_id: UUID


class AddUserToProject(BaseModel):
    project_id: UUID
    user_id: Optional[UUID] = None


class ProjectCreate(Project):
    creator_id: Optional[UUID] = None


class ProjectGet(Project):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    users: Optional[list[WithUser]] = []
    created_at: datetime
    updated_at: datetime


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
