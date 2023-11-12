from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.tasks.models import Task
from src.api_v1.tasks.schemas import TaskGet
from src.api_v1.tasks.views import get_task_by_id_handler, get_tasks_handler
from src.core.config import settings
from src.front.pages.auth.service import get_current_user_from_cookie
from src.utils.database import get_db
from src.utils.exceptions import EmptyAuthCookie

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/task/all", response_class=HTMLResponse)
async def task_all_page(request: Request, session: AsyncSession = Depends(get_db)):
    try:
        current_user: TokenUserData = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login",
            status_code=status.HTTP_302_FOUND,
        )
    if current_user:
        tasks: list[Task] = await get_tasks_handler(limit=5, offset=0, session=session)
    context = {
        "logged_in": True,
        "tasks": [TaskGet.model_validate(t) for t in tasks],
        "request": request,
    }
    return templates.TemplateResponse("task.html", context)


@router.get("/task/{task_id}", response_class=HTMLResponse)
async def task_page(
    request: Request, task_id: str, session: AsyncSession = Depends(get_db)
):
    try:
        current_user: TokenUserData = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        return RedirectResponse(
            url=f"{settings.front_prefix}/login",
            status_code=status.HTTP_302_FOUND,
        )
    if current_user:
        task: Task = await get_task_by_id_handler(
            task_id=task_id, session=session, current_user=current_user
        )
    context = {
        "logged_in": True,
        "single_task": True,
        "task": TaskGet.model_validate(task),
        "request": request,
    }
    return templates.TemplateResponse("task.html", context)
