import datetime
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from .base import Base


class Task(Base):
    title: sao.Mapped[str]
    description: sao.Mapped[str]
    status: sao.Mapped[str]
    priority: sao.Mapped[str]
    due_date: sao.Mapped[datetime.datetime]
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    updated_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)"),
        onupdate=sa.text("date_trunc('seconds', now()::timestamp)"),
    )

    user_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    project_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("projects.id", onupdate="CASCADE", ondelete="CASCADE")
    )


class TaskComment(Base):
    content: sao.Mapped[str]
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    user_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    task_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("tasks.id", onupdate="CASCADE", ondelete="CASCADE")
    )
