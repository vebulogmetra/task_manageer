from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.api_v1.associates.schemas import WithProject


class Team(BaseModel):
    title: str
    creator_id: UUID


class TeamCreate(Team):
    ...


class TeamGet(Team):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    projects: Optional[list[WithProject]] = []
    created_at: datetime


class TeamUpdate(Team):
    ...
