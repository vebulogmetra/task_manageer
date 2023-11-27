from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.tasks.models import Task
from src.api_v1.tasks.schemas import TaskGet
from src.api_v1.tasks.views import get_task_by_id_handler, get_tasks_handler
from src.core.config import html_templates
from src.front.helpers import auth as auth_helper
from src.front.helpers.responses import redirect_to_login
from src.front.helpers.schemas import AuthResponse
from src.utils.database import get_db

router = APIRouter()


@router.get("/task/all", response_class=HTMLResponse)
async def task_all_page(request: Request, session: AsyncSession = Depends(get_db)):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        tasks: list[Task] = await get_tasks_handler(limit=5, offset=0, session=session)
        context = {
            "logged_in": True,
            "tasks": [TaskGet.model_validate(t) for t in tasks],
            "request": request,
        }
        response = html_templates.TemplateResponse("task.html", context)
    return response


@router.get("/task/{task_id}", response_class=HTMLResponse)
async def task_page(
    request: Request, task_id: str, session: AsyncSession = Depends(get_db)
):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        task: Task = await get_task_by_id_handler(
            task_id=task_id, session=session, current_user=auth_data.current_user
        )

        context = {
            "logged_in": True,
            "single_task": True,
            "task": TaskGet.model_validate(task),
            "request": request,
        }
        response = html_templates.TemplateResponse("task.html", context)
    return response
