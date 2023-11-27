from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.dialogs.schemas import DialogGet, MessageGet, WithUser
from src.api_v1.dialogs.views import get_dialog_by_id_handler, get_dialogs_handler
from src.api_v1.users.models import User
from src.api_v1.users.schemas import GetUserFields
from src.api_v1.users.views import get_user_handler
from src.core.config import html_templates
from src.front.helpers import auth as auth_helper
from src.front.helpers.responses import redirect_to_login
from src.front.helpers.schemas import AuthResponse
from src.utils.database import get_db

router = APIRouter()


@router.get("/chat", response_class=HTMLResponse)
async def get_chat_page(request: Request, session: AsyncSession = Depends(get_db)):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        user: User = await get_user_handler(
            by_field=GetUserFields.id,
            by_value=str(auth_data.current_user.id),
            session=session,
            current_user=auth_data.current_user,
        )
        dialogs = await get_dialogs_handler(limit=10, offset=0, session=session)
        context = {"request": request, "user": user, "dialogs": dialogs}
        response = html_templates.TemplateResponse("chat.html", context)
    return response


@router.get("/chat/{dialog_id}", response_class=HTMLResponse)
async def get_dialog_by_id_page(
    request: Request, dialog_id: str, session: AsyncSession = Depends(get_db)
):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        dialog: dict = await get_dialog_by_id_handler(
            dialog_id=dialog_id, session=session, current_user=auth_data.current_user
        )
        user: User = await get_user_handler(
            by_field=GetUserFields.id,
            by_value=str(auth_data.current_user.id),
            session=session,
            current_user=auth_data.current_user,
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
            "logged_in": auth_data.is_auth_passed,
            "user": user,
            "dialog": DialogGet.model_validate(dialog),
            "request": request,
        }
        response = html_templates.TemplateResponse("chat.html", context)
    return response
