from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.base.models import Base

if TYPE_CHECKING:
    pass


class UserProject(Base):
    __tablename__ = "users_projects"
    __table_args__ = (
        sa.UniqueConstraint(
            "user_id",
            "project_id",
            name="unique_users_projects",
        ),
    )

    id: sao.Mapped[UUID] = sao.mapped_column(
        primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()")
    )
    user_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    project_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    # # association between Assocation -> Order
    # order: Mapped["Order"] = relationship(
    #     back_populates="products_details",
    # )
    # # association between Assocation -> Product
    # product: Mapped["Product"] = relationship(
    #     back_populates="orders_details",
    # )


class UserTask(Base):
    __tablename__ = "users_tasks"
    __table_args__ = (
        sa.UniqueConstraint(
            "user_id",
            "task_id",
            name="unique_users_tasks",
        ),
    )

    id: sao.Mapped[UUID] = sao.mapped_column(
        primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()")
    )
    user_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    task_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("tasks.id", ondelete="CASCADE", onupdate="CASCADE")
    )


class UserTeam(Base):
    __tablename__ = "users_teams"
    __table_args__ = (
        sa.UniqueConstraint(
            "user_id",
            "team_id",
            name="unique_users_teams",
        ),
    )

    id: sao.Mapped[UUID] = sao.mapped_column(
        primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()")
    )
    user_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    team_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("teams.id", ondelete="CASCADE", onupdate="CASCADE")
    )


class UserDialog(Base):
    __tablename__ = "users_dialogs"
    __table_args__ = (
        sa.UniqueConstraint(
            "user_id",
            "dialog_id",
            name="unique_users_dialogs",
        ),
    )

    id: sao.Mapped[UUID] = sao.mapped_column(
        primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()")
    )
    user_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    dialog_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("dialogs.id", ondelete="CASCADE", onupdate="CASCADE")
    )
