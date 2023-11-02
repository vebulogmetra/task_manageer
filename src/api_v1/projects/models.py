from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.associates.models import users_projects
from src.api_v1.base.models import Base

if TYPE_CHECKING:
    from src.api_v1.tasks.models import Task
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
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    updated_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)"),
        onupdate=sa.text("date_trunc('seconds', now()::timestamp)"),
    )

    tasks: sao.Mapped[list[Task]] = sao.relationship(
        back_populates="project", lazy="selectin"
    )
    users: sao.Mapped[list[User]] = sao.relationship(
        secondary=users_projects, back_populates="projects", lazy="selectin"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, user_id={self.creator_id})"  # noqa

    def __repr__(self):
        return str(self)
