from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer

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
    creator: Optional[WithUser] = None
    users: Optional[list[WithUser]] = []
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


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
