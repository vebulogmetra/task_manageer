import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.orm as sao

from .base import Base


class Project(Base):
    name: sao.Mapped[str] = sao.mapped_column(
        sa.String(128),
        server_default=sa.text(
            "CONCAT('New project ', substring(uuid_generate_v4()::text, 1, 5))"
        ),
    )

    description: sao.Mapped[str] = sao.mapped_column(sa.Text(), nullable=True)
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
