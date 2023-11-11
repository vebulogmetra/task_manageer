from fastapi import APIRouter

from src.front.pages.auth.views import router as auth_router
from src.front.pages.index.views import router as index_router
from src.front.pages.project.views import router as project_router
from src.front.pages.task.views import router as task_router
from src.front.pages.team.views import router as team_router
from src.front.pages.user.views import router as user_router

__all__ = "main_router"

main_router: APIRouter = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(index_router)
main_router.include_router(project_router)
main_router.include_router(task_router)
main_router.include_router(team_router)
main_router.include_router(user_router)
