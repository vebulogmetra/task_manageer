from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.base.models import Base

if TYPE_CHECKING:
    from src.api_v1.chat.models import Chat
    from src.api_v1.projects.models import Project
    from src.api_v1.tasks.models import Task
    from src.api_v1.teams.models import Team


class User(Base):
    email: sao.Mapped[str] = sao.mapped_column(sa.String(64), unique=True, nullable=False)
    username: sao.Mapped[str] = sao.mapped_column(
        sa.String(64), unique=True, nullable=False
    )
    hashed_password: sao.Mapped[Optional[str]] = sao.mapped_column(
        sa.String(256), nullable=False
    )
    first_name: sao.Mapped[str | None] = sao.mapped_column(sa.String(32))
    last_name: sao.Mapped[str | None] = sao.mapped_column(sa.String(32))
    position: sao.Mapped[str | None] = sao.mapped_column(sa.String(64))
    avatar_url: sao.Mapped[str | None] = sao.mapped_column(sa.String(256))
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

    created_projects: sao.Mapped[list[Project]] = sao.relationship(
        back_populates="creator", lazy="joined"
    )

    projects: sao.Mapped[list[Project]] = sao.relationship(
        secondary="users_projects", back_populates="users", lazy="joined"
    )

    tasks: sao.Mapped[list[Task]] = sao.relationship(
        secondary="users_tasks", back_populates="users", lazy="joined"
    )

    teams: sao.Mapped[list[Team]] = sao.relationship(
        secondary="users_teams", back_populates="users", lazy="joined"
    )

    chats: sao.Mapped[list[Chat]] = sao.relationship(
        secondary="users_chats", back_populates="participants", lazy="joined"
    )

    def __str__(self) -> str:
        return f"User {self.__table__.columns}"

    def __repr__(self):
        return f"User {self.username}"
