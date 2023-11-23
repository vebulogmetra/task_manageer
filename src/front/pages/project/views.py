from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.projects.models import Project
from src.api_v1.projects.schemas import ProjectGet
from src.api_v1.projects.views import get_project_by_id_handler, get_projects_handler
from src.front.helpers import auth as auth_helper
from src.front.helpers.responses import redirect_to_login
from src.front.helpers.schemas import AuthResponse
from src.utils.database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/project/all", response_class=HTMLResponse)
async def project_all_page(request: Request, session: AsyncSession = Depends(get_db)):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        projects: list[Project] = await get_projects_handler(
            limit=10,
            offset=0,
            session=session,
        )
        context = {
            "logged_in": True,
            "projects": [ProjectGet.model_validate(p) for p in projects],
            "request": request,
        }
        response = templates.TemplateResponse("project.html", context)
    return response


@router.get("/project/{project_id}", response_class=HTMLResponse)
async def project_page(
    request: Request, project_id: str, session: AsyncSession = Depends(get_db)
):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        project: Project = await get_project_by_id_handler(
            project_id=project_id, session=session, current_user=auth_data.current_user
        )
        context = {
            "logged_in": True,
            "single_project": True,
            "project": ProjectGet.model_validate(project),
            "request": request,
        }
        response = templates.TemplateResponse("project.html", context)
    return response
