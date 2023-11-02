from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.api_v1.associates.schemas import WithUser


class Project(BaseModel):
    name: str
    description: str
    creator_id: UUID


class ProjectCreate(Project):
    pass


class ProjectGet(Project):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    users: Optional[list[WithUser]]
    created_at: datetime
    updated_at: datetime


class ProjectUpdate(Project):
    pass
