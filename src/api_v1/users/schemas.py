from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    username: str


class UserGet(User):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime


class UserCreate(User):
    pass
