from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.front.pages.auth.service import get_current_user_from_cookie
from src.utils.exceptions import EmptyAuthCookie

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/team")
def get_team(request: Request):
    try:
        user = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        user = None
    context = {
        "users": [user],
        "team": {"title": "ABCTeam"},
        "request": request,
    }
    return templates.TemplateResponse("team.html", context)
