from __future__ import annotations

import datetime
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.base.models import Base


class Team(Base):
    title: sao.Mapped[str] = sao.mapped_column(sa.String(64), nullable=False)
    description: sao.Mapped[str] = sao.mapped_column(sa.Text(), nullable=True)
    creator_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
