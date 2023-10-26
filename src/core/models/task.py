import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.orm as sao

from .base import Base


class Task(Base):
    title: sao.Mapped[str] = sao.mapped_column(
        sa.String(128),
        default=f"New task {uuid4().hex[:5]}",
        server_default=sa.text(
            "CONCAT('New task ', substring(uuid_generate_v4()::text, 1, 5))"
        ),
    )
    description: sao.Mapped[str] = sao.mapped_column(
        sa.Text(), nullable=True, default="", server_default=""
    )
    status: sao.Mapped[str] = sao.mapped_column(
        sa.String(32), default="created", server_default="created"
    )
    priority: sao.Mapped[int] = sao.mapped_column(
        sa.Integer(), default=1, server_default=1
    )
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
