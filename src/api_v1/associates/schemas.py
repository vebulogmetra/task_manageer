from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class WithUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    position: str
    role: str
    avatar_url: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        if isinstance(created_at, datetime):
            return created_at.strftime("%d-%m-%Y %H:%M:%S")
        return created_at


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


class WithProject(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    creator_id: UUID
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


class WithTeam(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    creator_id: UUID
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        if isinstance(created_at, datetime):
            return created_at.strftime("%d-%m-%Y %H:%M:%S")
        return created_at
