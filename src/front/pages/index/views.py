from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.core.config import settings
from src.front.pages.auth.service import get_current_user_from_cookie
from src.utils.exceptions import EmptyAuthCookie

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/", response_class=HTMLResponse)
def get_index_page(request: Request):
    try:
        user = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        user = None
    if user:
        return RedirectResponse(
            url=f"{settings.front_prefix}/current_user", status_code=status.HTTP_302_FOUND
        )
    else:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login", status_code=status.HTTP_302_FOUND
        )


@router.get("/home", response_class=HTMLResponse)
def get_home_page(request: Request):
    try:
        user = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        user = None
    context = {
        "user": user,
        "request": request,
    }
    return templates.TemplateResponse("home.html", context)
