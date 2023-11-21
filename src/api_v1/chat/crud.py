from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api_v1.associates.models import UserChat
from src.api_v1.base.utils import is_valid_uuid
from src.api_v1.chat.models import Chat
from src.api_v1.chat.schemas import AddUserToChat, ChatCreate
from src.utils.exceptions import custom_exc


async def create_chat(db_session: AsyncSession, chat_data: ChatCreate) -> Chat:
    chat = Chat(**chat_data.model_dump())
    db_session.add(chat)
    await db_session.commit()
    await db_session.refresh(chat)
    return chat


async def add_user_to_chat(db_session: AsyncSession, data: AddUserToChat):
    user_chat = UserChat(**data.model_dump())
    db_session.add(user_chat)
    await db_session.commit()


async def get_chats(db_session: AsyncSession, limit: int, offset: int) -> list[Chat]:
    stmt = (
        select(Chat)
        # .options(joinedload(Chat.participants))
        .limit(limit)
        .offset(offset)
        .order_by(Chat.created_at)
    )
    result: Result = await db_session.execute(stmt)
    chats: list[Chat] = result.scalars().unique()
    if chats is None:
        raise custom_exc.not_found(entity_name=f"{Chat.__name__}s")
    return list(chats)


async def get_chat(db_session: AsyncSession, chat_id: UUID) -> Chat | None:
    is_uuid: bool = is_valid_uuid(value=chat_id)
    if is_uuid is False:
        raise custom_exc.invalid_input(detail="chat id must by valid type UUID4")
    stmt = select(Chat).options(joinedload(Chat.participants)).where(Chat.id == chat_id)
    result: Result = await db_session.execute(stmt)
    chat = result.scalar()
    if chat is None:
        raise custom_exc.not_found(entity_name=Chat.__name__)
    return chat
