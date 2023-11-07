from __future__ import annotations

import datetime
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.base.model_mixins import UserRelationMixin
from src.api_v1.base.models import Base


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

    def __repr__(self):
        return f"User {self.username}"


class UserProfile(Base, UserRelationMixin):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: sao.Mapped[str | None] = sao.mapped_column(sa.String(32))
    last_name: sao.Mapped[str | None] = sao.mapped_column(sa.String(32))
    avatar_url: sao.Mapped[str | None] = sao.mapped_column(sa.String(256))

    def __repr__(self):
        return f"Profile {self.first_name}"
