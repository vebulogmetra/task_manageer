from fastapi import APIRouter, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.dialogs.crud import get_dialog_by_members
from src.api_v1.dialogs.schemas import DialogCreate
from src.api_v1.dialogs.views import create_dialog_handler, get_dialogs_by_member_handler
from src.api_v1.users.models import User
from src.api_v1.users.schemas import GetUserFields
from src.api_v1.users.views import get_user_handler
from src.core.config import html_templates, settings
from src.front.helpers import auth as auth_helper
from src.front.helpers.responses import redirect_to_login
from src.front.helpers.schemas import AuthResponse
from src.utils.database import get_db

router = APIRouter()


def dialogs_to_json(dialogs: list) -> list[dict]:
    dialogs_clean = []
    for d in dialogs:
        # Удаляем hash пароля если есть
        dialog_dict: dict = jsonable_encoder(d)
        dialog_creator: dict = dialog_dict.get("creator", None)
        if dialog_creator:
            _ = dialog_creator.pop("hashed_password")
        dialogs_clean.append(dialog_dict)

    return dialogs_clean


@router.get("/dialogs")
async def show_dialogs_page(request: Request, session: AsyncSession = Depends(get_db)):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        user: User = await get_user_handler(
            by_field=GetUserFields.id,
            by_value=str(auth_data.current_user.id),
            session=session,
            current_user=auth_data.current_user,
        )

        dialogs: list[dict] = await get_dialogs_by_member_handler(
            limit=10, offset=0, session=session, current_user=auth_data.current_user
        )
        dialogs_dict: list[dict] = dialogs_to_json(dialogs=dialogs)
        user_dict: dict = jsonable_encoder(user)
        context = {
            "logged_in": True,
            "request": request,
            "user": user_dict,
            "dialogs": dialogs_dict,
        }
        response = html_templates.TemplateResponse("dialogs.html", context=context)
    return response


@router.get("/dialog/new/{creator_id}/{interlocutor_id}")
async def create_dialog(
    creator_id: str,
    interlocutor_id: str,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    # Проверяем есть ли диалог между пользователями
    dialog: dict = await get_dialog_by_members(
        db_session=session,
        user_1=str(creator_id),
        user_2=str(interlocutor_id),
    )
    if dialog is None:
        # Создаём новый диалог
        auth_data: AuthResponse = auth_helper.check_login(request=request)
        dialog_data: DialogCreate = DialogCreate(
            creator_id=creator_id, interlocutor_id=interlocutor_id
        )
        dialog = await create_dialog_handler(
            dialog_data=dialog_data,
            session=session,
            current_user=auth_data.current_user,
        )

    return RedirectResponse(
        url=f"{settings.front_prefix}/dialogs", status_code=status.HTTP_302_FOUND
    )
