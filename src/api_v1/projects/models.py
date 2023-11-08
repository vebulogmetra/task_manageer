from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.base.models import Base

if TYPE_CHECKING:
    from src.api_v1.users.models import User


class Project(Base):
    name: sao.Mapped[str] = sao.mapped_column(
        sa.String(128),
        server_default=sa.text(
            "CONCAT('New project ', substring(gen_random_uuid()::text, 1, 5))"
        ),
    )

    description: sao.Mapped[str] = sao.mapped_column(sa.Text(), nullable=True)
    creator_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    team_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("teams.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True
    )
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    updated_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)"),
        onupdate=sa.text("date_trunc('seconds', now()::timestamp)"),
    )

    users: sao.Mapped[list[User]] = sao.relationship(
        secondary="users_projects", back_populates="projects"
    )

    def __str__(self):
        return f"Project {self.name}"

    def __repr__(self):
        return str(self)
