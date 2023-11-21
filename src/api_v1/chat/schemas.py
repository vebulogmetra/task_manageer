from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer

from src.api_v1.associates.schemas import WithUser


class Message(BaseModel):
    sender_id: UUID
    content: str


class Chat(BaseModel):
    name: str


class ChatCreate(Chat):
    ...


class MessageCreate(Message):
    ...


class ChatGet(Chat):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    participants: Optional[list[WithUser]] = []
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
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        if isinstance(created_at, datetime):
            return created_at.strftime("%d-%m-%Y %H:%M:%S")
        return created_at


class AddUserToChat(BaseModel):
    chat_id: UUID
    user_id: Optional[UUID] = None
