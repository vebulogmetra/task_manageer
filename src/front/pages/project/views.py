from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.projects.models import Project
from src.api_v1.projects.schemas import ProjectGet
from src.api_v1.projects.views import get_project_by_id_handler, get_projects_handler
from src.core.config import settings
from src.front.pages.auth.service import get_current_user_from_cookie
from src.utils.database import get_db
from src.utils.exceptions import EmptyAuthCookie

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/project/all", response_class=HTMLResponse)
async def project_all_page(request: Request, session: AsyncSession = Depends(get_db)):
    try:
        current_user: TokenUserData = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login",
            status_code=status.HTTP_302_FOUND,
        )
    if current_user:
        projects: list[Project] = await get_projects_handler(
            limit=10,
            offset=0,
            session=session,
        )
    context = {
        "projects": [ProjectGet.model_validate(p) for p in projects],
        "request": request,
    }
    return templates.TemplateResponse("project.html", context)


@router.get("/project/{project_id}", response_class=HTMLResponse)
async def project_page(
    request: Request, project_id: str, session: AsyncSession = Depends(get_db)
):
    try:
        current_user: TokenUserData = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login",
            status_code=status.HTTP_302_FOUND,
        )
    if current_user:
        project: Project = await get_project_by_id_handler(
            project_id=project_id, session=session, current_user=current_user
        )
    context = {
        "project": ProjectGet.model_validate(project),
        "request": request,
    }
    return templates.TemplateResponse("project.html", context)
