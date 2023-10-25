import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.core.models.base import Base
from src.core.models.user import User


class Project(Base):
    name: sao.Mapped[str]
    description: sao.Mapped[str]
    user_id: sao.Mapped['User'] = sao.relationship(back_populates='projects')
    created_at: sao.Mapped[str] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
    updated_at: sao.Mapped[str] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )
