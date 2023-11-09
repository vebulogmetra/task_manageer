from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.base.models import Base

if TYPE_CHECKING:
    from src.api_v1.projects.models import Project


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
    projects: sao.Mapped[list[Project]] = sao.relationship(
        secondary="users_projects", back_populates="users", lazy="joined"
    )

    def __str__(self) -> str:
        return f"User {self.__table__.columns}"

    def __repr__(self):
        return f"User {self.username}"
