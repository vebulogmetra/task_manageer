from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.base.models import Base

if TYPE_CHECKING:
    from src.api_v1.users.models import User


class Task(Base):
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
    due_date: sao.Mapped[datetime.datetime] = sao.mapped_column(sa.DateTime())
    creator_id: sao.Mapped[UUID] = sao.mapped_column(sa.ForeignKey("users.id"))
    project_id: sao.Mapped[UUID] = sao.mapped_column(sa.ForeignKey("projects.id"))
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    updated_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)"),
        onupdate=sa.text("date_trunc('seconds', now()::timestamp)"),
    )
    users: sao.Mapped[list[User]] = sao.relationship(
        secondary="users_tasks", back_populates="tasks", lazy="joined"
    )
    comments: sao.Mapped[list[TaskComment]] = sao.relationship(
        "TaskComment", lazy="joined"
    )

    def __str__(self):
        return f"Task {self.__table__.columns}"

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
