from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api_v1.associates.models import UserDialog
from src.api_v1.base.utils import is_valid_uuid
from src.api_v1.chat.models import Dialog, Message
from src.api_v1.chat.schemas import AddUserToDialog, DialogCreate, MessageCreate
from src.utils.exceptions import custom_exc


async def create_dialog(db_session: AsyncSession, dialog_data: DialogCreate) -> Dialog:
    chat = Dialog(**dialog_data.model_dump())
    db_session.add(chat)
    await db_session.commit()
    await db_session.refresh(chat)
    return chat


async def add_user_to_dialog(db_session: AsyncSession, data: AddUserToDialog):
    user_dialog = UserDialog(**data.model_dump())
    db_session.add(user_dialog)
    await db_session.commit()


async def get_dialogs(db_session: AsyncSession, limit: int, offset: int) -> list[Dialog]:
    stmt = (
        select(Dialog)
        .options(joinedload(Dialog.members), joinedload(Dialog.messages))
        .limit(limit)
        .offset(offset)
        .order_by(Dialog.created_at)
    )
    result: Result = await db_session.execute(stmt)
    dialogs: list[Dialog] = result.scalars().unique()
    if dialogs is None:
        raise custom_exc.not_found(entity_name=f"{Dialog.__name__}s")
    return list(dialogs)


async def get_dialog(db_session: AsyncSession, dialog_id: UUID) -> Dialog | None:
    is_uuid: bool = is_valid_uuid(value=dialog_id)
    if is_uuid is False:
        raise custom_exc.invalid_input(detail="dialog id must by valid type UUID4")
    stmt = (
        select(Dialog)
        .options(joinedload(Dialog.members), joinedload(Dialog.messages))
        .where(Dialog.id == dialog_id)
    )
    result: Result = await db_session.execute(stmt)
    dialog = result.scalar()
    if dialog is None:
        raise custom_exc.not_found(entity_name=Dialog.__name__)
    return dialog


async def add_message(db_session: AsyncSession, message_data: MessageCreate) -> Message:
    msg = Message(**message_data.model_dump())
    db_session.add(msg)
    await db_session.commit()
    await db_session.refresh(msg)
    return msg
