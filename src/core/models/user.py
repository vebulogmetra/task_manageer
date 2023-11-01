from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
import sqlalchemy.orm as sao

from .base import Base

if TYPE_CHECKING:
    from src.core.models.user_profile import UserProfile


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

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username})"

    def __repr__(self):
        return str(self)
