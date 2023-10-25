import sqlalchemy as sa
import sqlalchemy.orm as sao
from typing import Optional

from src.core.models.base import Base


class User(Base):
    usename: sao.Mapped[str] = sao.mapped_column(sa.String(64), unique=True)
    hashed_password: sao.Mapped[Optional[str]] = sao.mapped_column(sa.String(256))
    created_at: sao.Mapped[str] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
