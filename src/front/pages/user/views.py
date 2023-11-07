from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.users.schemas import UserGet
from src.api_v1.users.views import get_user_by_id_handler, get_users_handler
from src.front.pages.auth.service import get_current_user_from_cookie
from src.utils.database import get_db
from src.utils.exceptions import EmptyAuthCookie

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/current_user")
def get_current_user_id(request: Request):
    try:
        user = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        user = None
    context = {
        "user": user,
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
        current_user = None
    if current_user:
        user: UserGet = await get_user_by_id_handler(
            user_id=user_id, session=session, user_data=current_user
        )
    context = {
        "user": user,
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
        users: list[UserGet] = await get_users_handler(
            session=session, user_data=current_user
        )
    context = {
        "users": users,
        "request": request,
    }
    return templates.TemplateResponse("search.html", context)
