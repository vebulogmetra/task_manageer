from typing import Optional

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.auth.service import get_current_user
from src.api_v1.base.schemas import StatusMsg
from src.api_v1.chat import crud
from src.api_v1.chat.schemas import AddUserToDialog, DialogCreate, MessageCreate
from src.utils.database import get_db
from src.utils.websocket import ws_manager

router = APIRouter()


# @router.post("/create", response_model=ChatGet)
@router.post("/create")
async def create_dialog_handler(
    dialog_data: DialogCreate,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    new_dialog = await crud.create_dialog(db_session=session, dialog_data=dialog_data)
    # add creator to dialog memebers
    data = AddUserToDialog(dialog_id=new_dialog.id, user_id=current_user.id)
    await crud.add_user_to_dialog(db_session=session, data=data)
    await session.refresh(new_dialog)
    return new_dialog


@router.post("/add_user", response_model=StatusMsg)
async def add_user_to_dialog_handler(
    data: AddUserToDialog,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if data.user_id is None:
        data.user_id = current_user.id
    await crud.add_user_to_dialog(db_session=session, data=data)
    return StatusMsg(
        status="ok",
        detail=f"User {data.user_id} added in dialog {data.dialog_id}",
    )


# @router.get("/chats", response_model=list[ChatGet])
@router.get("/dialogs")
async def get_dialogs_handler(
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_dialogs(db_session=session, limit=limit, offset=offset)


# @router.get("/chat", response_model=ChatGet)
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
        await ws_manager.broadcast(f"Client #{user_id} left the chat")
