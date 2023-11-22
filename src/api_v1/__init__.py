from fastapi import APIRouter

from src.api_v1.associates.models import UserDialog, UserProject, UserTask, UserTeam
from src.api_v1.auth.views import router as auth_router
from src.api_v1.base.models import Base
from src.api_v1.chat.models import Dialog, Message
from src.api_v1.chat.views import router as chat_router
from src.api_v1.projects.models import Project
from src.api_v1.projects.views import router as projects_router
from src.api_v1.tasks.models import Task, TaskComment
from src.api_v1.tasks.views import router as tasks_router
from src.api_v1.teams.models import Team
from src.api_v1.teams.views import router as teams_router
from src.api_v1.users.models import User
from src.api_v1.users.views import router as users_router

__all__ = (
    "Base",
    "Project",
    "Task",
    "TaskComment",
    "Team",
    "User",
    "UserProject",
    "UserTask",
    "UserTeam",
    "Dialog",
    "Message",
    "UserDialog",
)


main_router: APIRouter = APIRouter()

main_router.include_router(
    router=chat_router,
    prefix="/chat",
    tags=["Chat"],
)


main_router.include_router(
    router=auth_router,
    prefix="/auth",
    tags=["Auth"],
)

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

main_router.include_router(
    router=teams_router,
    prefix="/teams",
    tags=["Teams"],
)
