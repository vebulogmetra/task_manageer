import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.core.models.base import Base
from src.core.models.mixins import UserRelationMixin

if TYPE_CHECKING:
    from src.core.models.task import Task
    from src.core.models.user import User


class Project(Base, UserRelationMixin):
    _user_id_nullable = False
    _user_id_unique = False
    _user_back_populates = "projects"

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

    tasks: sao.Mapped[list["Task"]] = sao.relationship(back_populates="project")
