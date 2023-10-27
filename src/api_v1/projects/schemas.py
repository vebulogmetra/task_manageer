from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Project(BaseModel):
    name: str
    description: str
    user_id: UUID


class ProjectCreate(Project):
    pass


class ProjectGet(Project):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: str
    updated_at: str
