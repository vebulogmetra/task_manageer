from typing import Optional

from fastapi import FastAPI, Request
from sqladmin import Admin, BaseView, ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncEngine

from src.api_v1.projects.models import Project
from src.api_v1.tasks.models import Task, TaskComment
from src.api_v1.teams.models import Team
from src.api_v1.users.models import User
from src.core.config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username == settings.admin_username and password == settings.admin_password:
            request.session.update({"token": settings.admin_auth_secret[:8]})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token or token != settings.admin_auth_secret[:8]:
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.admin_auth_secret)


class AdminApplication:
    def __init__(self, server_app: FastAPI, db_engine: AsyncEngine):
        self._server_app = server_app
        self._db_engine = db_engine
        self._views_list = [UserAdmin, ProjectAdmin, TaskAdmin]

    def init(self) -> Admin:
        options = {"app": self._server_app, "engine": self._db_engine}
        if settings.admin_panel_login:
            options.update({"authentication_backend": authentication_backend})
        self._admin_app = Admin(**options)
        return self._admin_app

    def include_views(
        self, admin_app: Optional[Admin] = None, views: list[ModelView | BaseView] = None
    ):
        if admin_app:
            self._admin_app = admin_app
        if views:
            self._views_list.extend(views)
            self._views_list = tuple(set(self._views_list))

        for view in self._views_list:
            self._admin_app.add_view(view)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role]


class ProjectAdmin(ModelView, model=Project):
    column_list = [Project.id, Project.name, Project.creator_id]


class TeamAdmin(ModelView, model=Team):
    column_list = [Team.id, Team.title, Team.creator_id]


class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.title, Task.creator_id]


class TaskCommentAdmin(ModelView, model=TaskComment):
    column_list = [TaskComment.id, TaskComment.user_id, TaskComment.content]
