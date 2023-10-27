from fastapi import APIRouter

from src.api_v1.projects.views import router as projects_router
from src.api_v1.tasks.views import router as tasks_router
from src.api_v1.users.views import router as users_router

main_router: APIRouter = APIRouter()

main_router.include_router(
    router=users_router,
    prefix="/users",
    tags=["Users"],
)
main_router.include_router(
    router=projects_router,
    prefix="/projects",
    tags=["Projects"],
)
main_router.include_router(
    router=tasks_router,
    prefix="/tasks",
    tags=["Tasks"],
)
