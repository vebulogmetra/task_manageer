from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.associates.models import users_tasks
from src.api_v1.base.models import Base

if TYPE_CHECKING:
    from src.api_v1.projects.models import Project
    from src.api_v1.users.models import User


class Task(Base):
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
    due_date: sao.Mapped[datetime.datetime] = sao.mapped_column(sa.DateTime())
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

    project_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("projects.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    project: sao.Mapped[Project] = sao.relationship(back_populates="tasks")
    users: sao.Mapped[list[User]] = sao.relationship(
        secondary=users_tasks, back_populates="tasks", lazy="selectin"
    )
    comments: sao.Mapped[list[TaskComment]] = sao.relationship(
        back_populates="task", lazy="selectin"
    )


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
    task: sao.Mapped[Task] = sao.relationship(back_populates="comments")
