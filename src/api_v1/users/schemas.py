from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_serializer

from src.core.config import settings


class Roles(Enum):
    user = "user"
    admin = "admin"
    creator = "creator"


class GetUserFields(Enum):
    id = "id"
    username = "username"
    email = "email"


class Positions(Enum):
    developer = "developer"
    product_owner = "product_owner"
    product_manager = "product_manager"
    project_manager = "project_manager"
    backend_developer = "backend_developer"
    frontend_developer = "frontend_developer"
    ios_developer = "ios_developer"
    android_developer = "android_developer"
    fullstack_developer = "fullstack_developer"
    uxui_designer = "uxui_designer"
    devops_engineer = "devops_engineer"
    systems_analyst = "systems_analyst"
    systems_architect = "systems_architect"
    database_administrator = "database_administrator"
    quality_assurance__qa_ = "quality_assurance__qa_"


class AdminPositions(Enum):
    product_owner = "product_owner"
    product_manager = "product_manager"
    project_manager = "project_manager"


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(BaseUser):
    model_config = ConfigDict(use_enum_values=True)
    password: str
    role: Optional[Roles] = Roles.user
    position: Optional[str] = Positions.developer
    avatar_url: Optional[str] = settings.default_avatar
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = True


class UserGet(BaseUser):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    role: Roles
    position: str
    avatar_url: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        if isinstance(created_at, datetime):
            return created_at.strftime("%d-%m-%Y %H:%M:%S")
        return created_at


##### Попытка слепить динамическую модель для подгрузки joinedload ###### noqa

# def create_dynamic_user_model(options: GetUserOptions) -> BaseModel:
#     dynamic_fields = {}
#     if options.include_created_projects:
#         dynamic_fields['created_projects'] = Optional[list[str]]
#     if options.include_projects:
#         dynamic_fields['projects'] = Optional[list[str]]
#     if options.include_tasks:
#         dynamic_fields['tasks'] = Optional[list[str]]
#     if options.include_teams:
#         dynamic_fields['teams'] = Optional[list[str]]
#     if options.include_dialogs:
#         dynamic_fields['chats'] = Optional[list[str]]

#     return create_model("DynamicUserModel", **dynamic_fields, __base__=BaseUser)


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
