from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.chat.schemas import DialogGet, MessageGet, WithUser
from src.api_v1.chat.views import get_dialog_by_id_handler, get_dialogs_handler
from src.api_v1.users.models import User
from src.api_v1.users.schemas import GetUserFields
from src.api_v1.users.views import get_user_handler
from src.core.config import settings
from src.front.pages.auth.service import get_current_user_from_cookie
from src.utils.database import get_db
from src.utils.exceptions import EmptyAuthCookie

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/chat", response_class=HTMLResponse)
async def get_chat_page(request: Request, session: AsyncSession = Depends(get_db)):
    try:
        current_user: TokenUserData = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login",
            status_code=status.HTTP_302_FOUND,
        )
    if current_user:
        user: User = await get_user_handler(
            by_field=GetUserFields.id,
            by_value=str(current_user.id),
            session=session,
            current_user=current_user,
        )
        dialogs = await get_dialogs_handler(limit=10, offset=0, session=session)
    context = {"request": request, "user": user, "dialogs": dialogs}
    return templates.TemplateResponse("chat.html", context)


@router.get("/chat/{dialog_id}", response_class=HTMLResponse)
async def get_dialog_by_id_page(
    request: Request, dialog_id: str, session: AsyncSession = Depends(get_db)
):
    try:
        current_user = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login", status_code=status.HTTP_302_FOUND
        )
    dialog: dict = await get_dialog_by_id_handler(
        dialog_id=dialog_id, session=session, current_user=current_user
    )
    user: User = await get_user_handler(
        by_field=GetUserFields.id,
        by_value=str(current_user.id),
        session=session,
        current_user=current_user,
    )

    dialog_messages: list[dict] = dialog.get("messages", None)
    if dialog_messages:
        for msg in dialog_messages:
            msg["is_sender"] = str(msg["sender_id"]) == str(user.id)
            sender = msg.get("sender")
            sender.pop("hashed_password", None)
            sender = WithUser.model_validate(sender)
            msg = MessageGet.model_validate(msg)

    context = {
        "logged_in": True if current_user else False,
        "user": user,
        "dialog": DialogGet.model_validate(dialog),
        "request": request,
    }
    return templates.TemplateResponse("chat.html", context)
