from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from src.api_v1.associates.schemas import WithProject, WithTask


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


class UserProfile(BaseModel):
    first_name: str
    last_name: str


class UserProfileCreate(BaseModel):
    ...


class UserProfileGet(BaseModel):
    ...


class UserGet(User):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    profile: Optional[UserProfile] = {}
    projects: Optional[list[WithProject]] = []
    tasks: Optional[list[WithTask]] = []
    created_at: datetime


class SignupGet(BaseModel):
    verif_code: str
    new_user: UserGet


class UserUpdate(User):
    ...
