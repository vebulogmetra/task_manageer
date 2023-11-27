from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.teams.models import Team
from src.api_v1.teams.schemas import TeamGet
from src.api_v1.teams.views import get_team_handler, get_teams_handler
from src.core.config import html_templates
from src.front.helpers import auth as auth_helper
from src.front.helpers.responses import redirect_to_login
from src.front.helpers.schemas import AuthResponse
from src.utils.database import get_db

router = APIRouter()


@router.get("/team/all", response_class=HTMLResponse)
async def team_all_page(request: Request, session: AsyncSession = Depends(get_db)):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        teams: list[Team] = await get_teams_handler(limit=10, offset=0, session=session)
        context = {
            "logged_in": True,
            "teams": [TeamGet.model_validate(t) for t in teams],
            "request": request,
        }
        response = html_templates.TemplateResponse("team.html", context)
    return response


@router.get("/team/{team_id}", response_class=HTMLResponse)
async def team_page(
    request: Request, team_id: str, session: AsyncSession = Depends(get_db)
):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        team: Team = await get_team_handler(
            team_id=team_id, session=session, current_user=auth_data.current_user
        )
        context = {
            "logged_in": True,
            "single_team": True,
            "team": TeamGet.model_validate(team),
            "request": request,
        }
        response = html_templates.TemplateResponse("team.html", context)
    return response
