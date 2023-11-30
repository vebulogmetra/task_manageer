from typing import Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, or_, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api_v1.base.utils import is_valid_uuid
from src.api_v1.dialogs.models import Dialog, Message
from src.api_v1.dialogs.schemas import DialogCreate, MessageCreate
from src.utils.exceptions import custom_exc


async def create_dialog(db_session: AsyncSession, dialog_data: DialogCreate) -> Dialog:
    dialog = Dialog(**dialog_data.model_dump())
    db_session.add(dialog)
    await db_session.commit()
    await db_session.refresh(dialog)
    return dialog


async def get_total_dialogs(db_session: AsyncSession) -> int:
    total_dialogs: int = await db_session.scalar(select(func.count(Dialog.id)))
    return total_dialogs


async def get_dialogs(
    db_session: AsyncSession,
    limit: int,
    offset: int,
    by_field: Optional[str] = None,
    by_value: Optional[UUID] = None,
) -> list[Dialog]:
    if by_value:
        is_uuid: bool = is_valid_uuid(value=by_value)
        if is_uuid is False:
            raise custom_exc.invalid_input(
                detail=f"{by_field} id must by valid type UUID4"
            )

    query = (
        select(Dialog)
        .options(
            selectinload(Dialog.creator),
            selectinload(Dialog.interlocutor),
            selectinload(Dialog.messages),
        )
        .limit(limit)
        .offset(offset)
        .order_by(Dialog.created_at)
    )

    if by_field and by_value:
        query = query.where(getattr(Dialog, by_field) == by_value)

    result = await db_session.execute(query)
    dialogs = result.scalars().unique()
    if not dialogs:
        raise custom_exc.not_found(entity_name=f"{Dialog.__name__}s")
    dialogs_clean = []
    for d in dialogs:
        dialog_dict: dict = jsonable_encoder(d)
        dialog_creator: dict = dialog_dict.get("creator", None)
        if dialog_creator:
            _ = dialog_creator.pop("hashed_password")
        dialogs_clean.append(dialog_dict)
    return dialogs_clean


async def get_dialogs_by_member(
    db_session: AsyncSession, limit: int, offset: int, member_id: UUID
) -> list[Dialog]:
    is_uuid: bool = is_valid_uuid(value=member_id)
    if is_uuid is False:
        raise custom_exc.invalid_input(detail="member id must by valid type UUID4")

    query = (
        select(Dialog)
        .options(
            selectinload(Dialog.creator),
            selectinload(Dialog.interlocutor),
            selectinload(Dialog.messages),
        )
        .limit(limit)
        .offset(offset)
        .order_by(Dialog.created_at)
    )
    query = query.where(
        or_(Dialog.creator_id == member_id, Dialog.interlocutor_id == member_id)
    )

    result = await db_session.execute(query)
    dialogs = result.scalars().unique()
    if not dialogs:
        raise custom_exc.not_found(entity_name=f"{Dialog.__name__}s")
    dialogs_clean = []
    for d in dialogs:
        dialog_dict: dict = jsonable_encoder(d)
        dialog_creator: dict = dialog_dict.get("creator", None)
        if dialog_creator:
            _ = dialog_creator.pop("hashed_password")
        dialogs_clean.append(dialog_dict)
    return dialogs_clean


async def get_dialog(db_session: AsyncSession, dialog_id: UUID) -> Dialog | None:
    is_uuid: bool = is_valid_uuid(value=dialog_id)
    if is_uuid is False:
        raise custom_exc.invalid_input(detail="dialog id must by valid type UUID4")
    stmt = (
        select(Dialog)
        .options(
            selectinload(Dialog.creator),
            selectinload(Dialog.interlocutor),
            selectinload(Dialog.messages),
        )
        .where(Dialog.id == dialog_id)
    )
    result: Result = await db_session.execute(stmt)
    dialog = result.scalar()
    if dialog is None:
        raise custom_exc.not_found(entity_name=Dialog.__name__)
    dialog_dict: dict = jsonable_encoder(dialog)
    dialog_creator: dict = dialog_dict.get("creator", None)
    if dialog_creator:
        _ = dialog_creator.pop("hashed_password")
    return dialog_dict


async def add_message(db_session: AsyncSession, message_data: MessageCreate) -> Message:
    msg = Message(**message_data.model_dump())
    db_session.add(msg)
    await db_session.commit()
    await db_session.refresh(msg)
    return msg
