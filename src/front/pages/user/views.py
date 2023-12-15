from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.users.models import User
from src.api_v1.users.schemas import GetUserFields, UserGet
from src.api_v1.users.views import (
    get_total_users_count_handler,
    get_user_handler,
    get_users_handler,
)
from src.core.config import html_templates
from src.front.helpers import auth as auth_helper
from src.front.helpers.responses import redirect_to_login
from src.front.helpers.schemas import AuthResponse
from src.utils.database import get_db

router = APIRouter()


@router.get("/account")
async def show_user_accont_page(
    request: Request, session: AsyncSession = Depends(get_db)
):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        user: User = await get_user_handler(
            session=session, current_user=auth_data.current_user
        )
        context = {
            "logged_in": True,
            "user": UserGet.model_validate(user),
            "request": request,
        }
        response = html_templates.TemplateResponse("account.html", context)
    return response


@router.get("/user/all", response_class=HTMLResponse)
async def show_users_page(
    request: Request,
    page: int = 1,
    items: int = 4,
    session: AsyncSession = Depends(get_db),
):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        offset: int = (page - 1) * items
        total_users: int = await get_total_users_count_handler(session=session)
        total_pages: int = (total_users // items) + 1

        users: list[User] = await get_users_handler(
            session=session,
            limit=items,
            offset=offset,
            _=auth_data.current_user,
        )
        context = {
            "logged_in": True,
            "users": [UserGet.model_validate(u) for u in users],
            "page": page,
            "total_pages": total_pages,
            "current_user": auth_data.current_user,
            "request": request,
        }
        response = html_templates.TemplateResponse("user.html", context)
    return response


@router.get("/user/{user_id}", response_class=HTMLResponse)
async def show_user_page(
    request: Request, user_id: str, session: AsyncSession = Depends(get_db)
):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        user: User = await get_user_handler(
            by_field=GetUserFields.id,
            by_value=user_id,
            session=session,
            current_user=auth_data.current_user,
        )
        context = {
            "logged_in": True,
            "user": UserGet.model_validate(user),
            "current_user": auth_data.current_user,
            "request": request,
        }
        response = html_templates.TemplateResponse("user.html", context)
    return response


# @router.get("/search", response_class=HTMLResponse)
# async def user_search_page(request: Request, session: AsyncSession = Depends(get_db)):
#     try:
#         current_user: TokenUserData = get_current_user_from_cookie(request)
#     except EmptyAuthCookie:
#         current_user = None
#     if current_user:
#         users: list[User] = await get_users_handler(session=session, _=current_user)
#     context = {
#         "logged_in": True,
#         "users": [UserGet.model_validate(u) for u in users],
#         "request": request,
#     }
#     return html_templates.TemplateResponse("search.html", context)
