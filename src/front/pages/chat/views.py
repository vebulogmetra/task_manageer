from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.core.config import settings
from src.front.pages.auth.service import get_current_user_from_cookie
from src.utils.exceptions import EmptyAuthCookie

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/chat", response_class=HTMLResponse)
def get_chat_page(request: Request):
    try:
        current_user = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        current_user = None
    if current_user:
        # Get chat data from db

        return RedirectResponse(
            url=f"{settings.front_prefix}/account", status_code=status.HTTP_302_FOUND
        )
    else:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login", status_code=status.HTTP_302_FOUND
        )


@router.get("/chat/{chat_id}", response_class=HTMLResponse)
def get_chat_by_id_page(request: Request):
    try:
        current_user = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        current_user = None
    context = {
        "logged_in": True if current_user else False,
        "user": current_user,
        "request": request,
    }
    return templates.TemplateResponse("home.html", context)
