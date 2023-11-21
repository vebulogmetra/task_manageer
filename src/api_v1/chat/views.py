from typing import Optional

from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.auth.service import get_current_user
from src.api_v1.base.schemas import StatusMsg
from src.api_v1.chat import crud
from src.api_v1.chat.schemas import AddUserToChat, ChatCreate
from src.utils.database import get_db

router = APIRouter()


# @router.post("/create", response_model=ChatGet)
@router.post("/create")
async def create_chat_handler(
    chat_data: ChatCreate,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_chat(db_session=session, chat_data=chat_data)


@router.post("/add_user", response_model=StatusMsg)
async def add_user_to_chat_handler(
    data: AddUserToChat,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if data.user_id is None:
        data.user_id = current_user.id
    await crud.add_user_to_chat(db_session=session, data=data)
    return StatusMsg(
        status="ok",
        detail=f"User {data.user_id} added in chat {data.chat_id}",
    )


# @router.get("/chats", response_model=list[ChatGet])
@router.get("/chats")
async def get_chats_handler(
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_chats(db_session=session, limit=limit, offset=offset)


# @router.get("/chat", response_model=ChatGet)
@router.get("/chat")
async def get_chat_by_id_handler(
    chat_id: str,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    chat = await crud.get_chat(db_session=session, chat_id=chat_id)
    return chat


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
