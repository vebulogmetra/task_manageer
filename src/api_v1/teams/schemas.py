from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer

from src.api_v1.associates.schemas import WithUser


class Team(BaseModel):
    title: str
    description: str
    creator_id: UUID


class TeamCreate(Team):
    creator_id: Optional[UUID] = None


class AddUserToTeam(BaseModel):
    team_id: UUID
    user_id: Optional[UUID] = None


class TeamGet(Team):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    users: Optional[list[WithUser]] = []
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        if isinstance(created_at, datetime):
            return created_at.strftime("%d-%m-%Y %H:%M:%S")
        return created_at


class TeamUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
