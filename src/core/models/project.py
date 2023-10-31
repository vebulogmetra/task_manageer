import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.task import Task


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

    tasks: sao.Mapped[list["Task"]] = sao.relationship(back_populates="project")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, user_id={self.creator_id})"  # noqa

    def __repr__(self):
        return str(self)
