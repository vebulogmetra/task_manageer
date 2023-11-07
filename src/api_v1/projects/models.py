from __future__ import annotations

import datetime
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.base.models import Base


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

    def __str__(self):
        return f"Project {self.name}"

    def __repr__(self):
        return str(self)
