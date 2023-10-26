from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from api_v1.projects.schemas import ProjectGet
from api_v1.tasks.schemas import TaskGet


class User(BaseModel):
    username: str


class UserGet(User):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    # projects: list[ProjectGet]
    # tasks: list[TaskGet]


class UserCreate(User):
    pass
