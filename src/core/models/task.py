import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.core.models.mixins import UserRelationMixin

from .base import Base

if TYPE_CHECKING:
    from src.core.models.project import Project


class Task(Base, UserRelationMixin):
    _user_back_populates = "tasks"

    title: sao.Mapped[str] = sao.mapped_column(
        sa.String(128),
        # default=f"New task {uuid4().hex[:5]}",
        server_default=sa.text("concat('New task ', substr(md5(random()::text), 1,5))"),
    )
    description: sao.Mapped[str] = sao.mapped_column(sa.Text(), nullable=True)
    status: sao.Mapped[str] = sao.mapped_column(
        sa.String(32), default="created", server_default="created"
    )  # created, in_work, complete
    priority: sao.Mapped[str] = sao.mapped_column(
        sa.String(), default="low", server_default="low"
    )  # low, medium, high
    due_date: sao.Mapped[datetime.datetime]
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    updated_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)"),
        onupdate=sa.text("date_trunc('seconds', now()::timestamp)"),
    )

    project_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("projects.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    project: sao.Mapped["Project"] = sao.relationship(back_populates="tasks")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, \
title={self.title}, user_id={self.user_id}, project_id={self.project_id})"

    def __repr__(self):
        return str(self)


class TaskComment(Base):
    content: sao.Mapped[str] = sao.mapped_column(sa.String(256))
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    user_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    task_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("tasks.id", onupdate="CASCADE", ondelete="CASCADE")
    )
