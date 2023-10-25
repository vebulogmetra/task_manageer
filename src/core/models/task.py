import datetime
import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.core.models.base import Base
from src.core.models.user import User
from src.core.models.project import Project


class Task(Base):
    title: sao.Mapped[str]
    description: sao.Mapped[str]
    status: sao.Mapped[str]
    priority: sao.Mapped[str]
    due_date: sao.Mapped[datetime.datetime]
    created_at: sao.Mapped[str] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    updated_at: sao.Mapped[str] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )

    user_id: sao.Mapped['User'] = sao.relationship(back_populates='tasks')
    project_id: sao.Mapped['Project'] = sao.relationship(back_populates='tasks')


class TaskComment(Base):
    content: sao.Mapped[str]
    created_at: sao.Mapped[str] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    user_id: sao.Mapped['User'] = sao.relationship(back_populates='taskcomments')
    task_id: sao.Mapped['Task'] = sao.relationship(back_populates='taskcomments')
