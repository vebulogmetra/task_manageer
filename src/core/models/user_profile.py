import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.core.models.mixins import UserRelationMixin

from .base import Base


class UserProfile(Base, UserRelationMixin):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: sao.Mapped[str | None] = sao.mapped_column(sa.String(32))
    last_name: sao.Mapped[str | None] = sao.mapped_column(sa.String(32))
