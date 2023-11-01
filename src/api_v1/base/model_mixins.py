from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

if TYPE_CHECKING:
    from src.api_v1.users.models import User


class UserRelationMixin:
    _user_id_unique: bool = False
    _user_id_nullable: bool = False
    _user_back_populates: str | None = None

    @declared_attr
    def user_id(cls):
        return mapped_column(
            ForeignKey("users.id"),
            unique=cls._user_id_unique,
            nullable=cls._user_id_nullable,
        )

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship(
            "User",
            back_populates=cls._user_back_populates,
        )
