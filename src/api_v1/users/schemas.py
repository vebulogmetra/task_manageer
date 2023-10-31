from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class Roles(Enum):
    user = "user"
    admin = "admin"
    creator = "creator"


class User(BaseModel):
    username: str
    email: EmailStr
    role: Roles
    is_active: bool
    is_verified: bool


class UserCreate(User):
    password: str
    role: Optional[Roles] = Roles.user
    is_active: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserGet(User):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime


class UserUpdate(User):
    pass
