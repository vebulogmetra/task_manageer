from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.users.models import User
from src.api_v1.users.schemas import GetUserFields, UserGet
from src.api_v1.users.views import (
    get_total_users_count_handler,
    get_user_handler,
    get_users_handler,
)
from src.core.config import settings
from src.front.pages.auth.service import get_current_user_from_cookie
from src.utils.database import get_db
from src.utils.exceptions import EmptyAuthCookie

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/account")
async def get_current_user_id(request: Request, session: AsyncSession = Depends(get_db)):
    try:
        current_user = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login",
            status_code=status.HTTP_302_FOUND,
        )
    if current_user:
        user: User = await get_user_handler(session=session, current_user=current_user)
    context = {
        "logged_in": True,
        "user": UserGet.model_validate(user),
        "request": request,
    }
    return templates.TemplateResponse("account.html", context)


@router.get("/user/all", response_class=HTMLResponse)
async def user_all_page(
    request: Request,
    page: int = 1,
    items: int = 4,
    session: AsyncSession = Depends(get_db),
):
    try:
        current_user: TokenUserData = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login",
            status_code=status.HTTP_302_FOUND,
        )
    offset: int = (page - 1) * items
    total_users: int = await get_total_users_count_handler(session=session)
    total_pages: int = (total_users // items) + 1

    if current_user:
        users: list[User] = await get_users_handler(
            session=session,
            limit=items,
            offset=offset,
            _=current_user,
        )
    context = {
        "logged_in": True,
        "users": [UserGet.model_validate(u) for u in users],
        "page": page,
        "total_pages": total_pages,
        "request": request,
    }
    return templates.TemplateResponse("user.html", context)


@router.get("/user/{user_id}", response_class=HTMLResponse)
async def user_page(
    request: Request, user_id: str, session: AsyncSession = Depends(get_db)
):
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
            by_value=user_id,
            session=session,
            current_user=current_user,
        )
    context = {
        "logged_in": True,
        "user": UserGet.model_validate(user),
        "request": request,
    }
    return templates.TemplateResponse("user.html", context)


@router.get("/search", response_class=HTMLResponse)
async def user_search_page(request: Request, session: AsyncSession = Depends(get_db)):
    try:
        current_user: TokenUserData = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        current_user = None
    if current_user:
        users: list[User] = await get_users_handler(session=session, _=current_user)
    context = {
        "logged_in": True,
        "users": [UserGet.model_validate(u) for u in users],
        "request": request,
    }
    return templates.TemplateResponse("search.html", context)
