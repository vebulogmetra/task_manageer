from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.associates.models import users_projects, users_tasks
from src.api_v1.base.model_mixins import UserRelationMixin
from src.api_v1.base.models import Base

if TYPE_CHECKING:
    from src.api_v1.projects.models import Project
    from src.api_v1.tasks.models import Task


class User(Base):
    username: sao.Mapped[str] = sao.mapped_column(
        sa.String(64), unique=True, nullable=False
    )
    email: sao.Mapped[str] = sao.mapped_column(sa.String(64), unique=True, nullable=False)
    hashed_password: sao.Mapped[Optional[str]] = sao.mapped_column(
        sa.String(256), nullable=False
    )
    role: sao.Mapped[str] = sao.mapped_column(
        sa.String(32), default="user", nullable=False
    )
    is_active: sao.Mapped[bool] = sao.mapped_column(
        sa.Boolean, default=False, nullable=False
    )
    is_verified: sao.Mapped[bool] = sao.mapped_column(
        sa.Boolean, default=False, nullable=False
    )
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    profile: sao.Mapped[UserProfile] = sao.relationship(back_populates="user")
    projects: sao.Mapped[list[Project]] = sao.relationship(
        secondary=users_projects, back_populates="users"
    )
    tasks: sao.Mapped[list[Task]] = sao.relationship(
        secondary=users_tasks, back_populates="users"
    )


class UserProfile(Base, UserRelationMixin):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: sao.Mapped[str | None] = sao.mapped_column(sa.String(32))
    last_name: sao.Mapped[str | None] = sao.mapped_column(sa.String(32))
