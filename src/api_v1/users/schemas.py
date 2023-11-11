from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_serializer

from src.api_v1.associates.schemas import WithProject, WithTask, WithTeam


class Roles(Enum):
    user = "user"
    admin = "admin"
    creator = "creator"


class GetUserFields(Enum):
    id = "id"
    username = "username"
    email = "email"


class User(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: str
    avatar_url: Optional[str] = None
    role: Roles
    is_active: bool
    is_verified: bool


class UserCreate(User):
    password: str
    role: Optional[Roles] = Roles.user
    position: Optional[str] = "developer"
    avatar_url: Optional[str] = "default.png"
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = True


class UserGet(User):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_projects: Optional[list[WithProject]] = []
    projects: Optional[list[WithProject]] = []
    tasks: Optional[list[WithTask]] = []
    teams: Optional[list[WithTeam]] = []
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        if isinstance(created_at, datetime):
            return created_at.strftime("%d-%m-%Y %H:%M:%S")
        return created_at


class SignupGet(BaseModel):
    verif_code: str
    new_user: UserGet


class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[Roles] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
