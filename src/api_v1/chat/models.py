from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.base.models import Base

if TYPE_CHECKING:
    from src.api_v1.users.models import User


class ChatMessage(Base):
    chat_id: sao.Mapped[UUID] = sao.mapped_column(sa.ForeignKey("chats.id"))
    sender_id: sao.Mapped[UUID] = sao.mapped_column(sa.ForeignKey("users.id"))
    content: sao.Mapped[str] = sao.mapped_column(sa.String(120), nullable=True)
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )

    sender: sao.Mapped[User] = sao.relationship()


class Chat(Base):
    name: sao.Mapped[str] = sao.mapped_column(
        sa.String(32),
        server_default=sa.text(
            "CONCAT('New chat ', substring(gen_random_uuid()::text, 1, 5))"
        ),
    )
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )

    participants: sao.Mapped[list[User]] = sao.relationship(
        secondary="users_chats", back_populates="chats"
    )

    messages: sao.Mapped[list[ChatMessage]] = sao.relationship()

    def __str__(self):
        return f"Chat {self.__table__.columns}"

    def __repr__(self):
        return str(self)
