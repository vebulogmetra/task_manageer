from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.teams.models import Team
from src.api_v1.teams.schemas import TeamGet
from src.api_v1.teams.views import get_team_handler, get_teams_handler
from src.core.config import settings
from src.front.pages.auth.service import get_current_user_from_cookie
from src.utils.database import get_db
from src.utils.exceptions import EmptyAuthCookie

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/team/all", response_class=HTMLResponse)
async def team_all_page(request: Request, session: AsyncSession = Depends(get_db)):
    try:
        current_user: TokenUserData = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login",
            status_code=status.HTTP_302_FOUND,
        )
    if current_user:
        teams: list[Team] = await get_teams_handler(limit=10, offset=0, session=session)
    context = {
        "teams": [TeamGet.model_validate(t) for t in teams],
        "request": request,
    }
    return templates.TemplateResponse("team.html", context)


@router.get("/team/{team_id}", response_class=HTMLResponse)
async def team_page(
    request: Request, team_id: str, session: AsyncSession = Depends(get_db)
):
    try:
        current_user: TokenUserData = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login",
            status_code=status.HTTP_302_FOUND,
        )
    if current_user:
        team: Team = await get_team_handler(
            team_id=team_id, session=session, current_user=current_user
        )
    context = {
        "team": TeamGet.model_validate(team),
        "request": request,
    }
    return templates.TemplateResponse("team.html", context)
