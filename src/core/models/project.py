import datetime
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from .base import Base


class Project(Base):
    name: sao.Mapped[str]
    description: sao.Mapped[str]
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
