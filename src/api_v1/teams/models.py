from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.associates.models import users_teams
from src.api_v1.base.models import Base

if TYPE_CHECKING:
    from src.api_v1.users.models import User


class Team(Base):
    title: sao.Mapped[str] = sao.mapped_column(sa.String(64), nullable=False)
    creator_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )

    users: sao.Mapped[list[User]] = sao.relationship(
        secondary=users_teams, back_populates="teams", lazy="selectin"
    )
