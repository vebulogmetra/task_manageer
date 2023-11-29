from typing import Optional

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.auth.service import get_current_user
from src.api_v1.base.schemas import StatusMsg
from src.api_v1.dialogs import crud
from src.api_v1.dialogs.schemas import DialogCreate, DialogGet, MessageCreate
from src.utils.database import get_db
from src.utils.websocket import ws_manager

router = APIRouter()


@router.post("/create")
async def create_dialog_handler(
    dialog_data: DialogCreate,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if dialog_data.creator_id is None:
        dialog_data.creator_id = current_user.id

    new_dialog = await crud.create_dialog(db_session=session, dialog_data=dialog_data)
    return new_dialog


@router.get("/dialogs", response_model=list[DialogGet])
async def get_dialogs_handler(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_dialogs(db_session=session, limit=limit, offset=offset)


@router.get("/dialogs_by_creator")
async def get_dialogs_by_creator_handler(
    creator_id: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if creator_id is None:
        creator_id = current_user.id
    return await crud.get_dialogs(
        db_session=session,
        limit=limit,
        offset=offset,
        by_field="creator_id",
        by_value=creator_id,
    )


@router.get("/dialogs_by_interlocutor")
async def get_dialogs_by_interlocutor_handler(
    interlocutor_id: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if interlocutor_id is None:
        interlocutor_id = current_user.id
    return await crud.get_dialogs(
        db_session=session,
        limit=limit,
        offset=offset,
        by_field="interlocutor_id",
        by_value=interlocutor_id,
    )


@router.get("/dialogs_by_member")
async def get_dialogs_by_member_handler(
    member_id: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if member_id is None:
        member_id = current_user.id
    return await crud.get_dialogs_by_member(
        db_session=session, limit=limit, offset=offset, member_id=member_id
    )


@router.get("/dialog")
async def get_dialog_by_id_handler(
    dialog_id: str,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    dialog = await crud.get_dialog(db_session=session, dialog_id=dialog_id)
    return dialog


@router.post("/add_message")
async def add_message_handler(
    message_data: MessageCreate,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if message_data.sender_id is None:
        message_data.sender_id = current_user.id

    await crud.add_message(db_session=session, message_data=message_data)
    return StatusMsg(
        status="ok",
        detail=f"Message '{message_data.content}' \
added in dialog {message_data.dialog_id}",
    )


@router.websocket("/ws/{dialog_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    dialog_id: str,
    user_id: str,
    session: AsyncSession = Depends(get_db),
):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await ws_manager.send_personal_message(f"You wrote: {data}", websocket)
            await ws_manager.broadcast(f"{data}")
            message_data: MessageCreate = MessageCreate(
                dialog_id=dialog_id, sender_id=user_id, content=data
            )
            await crud.add_message(db_session=session, message_data=message_data)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        await ws_manager.broadcast(f"Client #{user_id} left the dialog")
