from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    username: str


class UserCreate(User):
    password: str


class UserGet(User):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime


class UserUpdate(User):
    pass
