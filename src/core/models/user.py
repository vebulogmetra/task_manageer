import datetime
from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
import sqlalchemy.orm as sao

from .base import Base

if TYPE_CHECKING:
    from src.core.models.project import Project
    from src.core.models.task import Task
    from src.core.models.user_profile import UserProfile


class User(Base):
    username: sao.Mapped[str] = sao.mapped_column(sa.String(64), unique=True)
    hashed_password: sao.Mapped[Optional[str]] = sao.mapped_column(sa.String(256))
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    profile: sao.Mapped["UserProfile"] = sao.relationship(back_populates="user")
    projects: sao.Mapped[list["Project"]] = sao.relationship(back_populates="user")
    tasks: sao.Mapped[list["Task"]] = sao.relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username})"

    def __repr__(self):
        return str(self)
