from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.api_v1.base.models import Base

if TYPE_CHECKING:
    from src.api_v1.users.models import User


class Message(Base):
    dialog_id: sao.Mapped[UUID] = sao.mapped_column(sa.ForeignKey("dialogs.id"))
    sender_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE")
    )
    content: sao.Mapped[str] = sao.mapped_column(sa.String(120), nullable=True)
    send_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )

    sender: sao.Mapped[User] = sao.relationship(
        "User", foreign_keys=[sender_id], lazy="selectin"
    )


class Dialog(Base):
    creator_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE")
    )
    interlocutor_id: sao.Mapped[UUID] = sao.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE")
    )
    created_at: sao.Mapped[datetime.datetime] = sao.mapped_column(
        server_default=sa.text("date_trunc('seconds', now()::timestamp)")
    )

    messages: sao.Mapped[list[Message]] = sao.relationship(
        "Message", order_by="Message.send_at.asc()"
    )

    creator: sao.Mapped[User] = sao.relationship("User", foreign_keys=[creator_id])
    interlocutor: sao.Mapped[User] = sao.relationship(
        "User", foreign_keys=[interlocutor_id]
    )

    def __str__(self):
        return f"Dialog {self.__table__.columns}"

    def __repr__(self):
        return str(self)
