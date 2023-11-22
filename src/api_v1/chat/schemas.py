from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer

from src.api_v1.associates.schemas import WithUser


class Message(BaseModel):
    dialog_id: UUID
    sender_id: UUID
    content: str


class Dialog(BaseModel):
    name: str


class DialogCreate(Dialog):
    ...


class MessageCreate(Message):
    sender_id: Optional[UUID] = None


class DialogGet(Dialog):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    members: Optional[list[WithUser]] = []
    messages: Optional[list[Message]] = []
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        if isinstance(created_at, datetime):
            return created_at.strftime("%d-%m-%Y %H:%M:%S")
        return created_at


class MessageGet(Message):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    sender: WithUser
    send_at: datetime

    @field_serializer("send_at")
    def serialize_send_at(self, send_at: datetime):
        if isinstance(send_at, datetime):
            return send_at.strftime("%d-%m-%Y %H:%M:%S")
        return send_at


class AddUserToDialog(BaseModel):
    dialog_id: UUID
    user_id: Optional[UUID] = None
