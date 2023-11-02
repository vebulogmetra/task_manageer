from typing import Optional

from fastapi import FastAPI
from sqladmin import Admin, BaseView, ModelView
from sqlalchemy.ext.asyncio import AsyncEngine

from src.api_v1.projects.models import Project
from src.api_v1.tasks.models import Task, TaskComment
from src.api_v1.users.models import User


class AdminApplication:
    def __init__(self, server_app: FastAPI, db_engine: AsyncEngine):
        self._server_app = server_app
        self._db_engine = db_engine
        self._views_list = (UserAdmin, ProjectAdmin, TaskAdmin)

    def init(self) -> Admin:
        self._admin_app = Admin(self._server_app, self._db_engine)
        return self._admin_app

    def include_views(
        self, admin_app: Optional[Admin] = None, views: list[ModelView | BaseView] = None
    ):
        if admin_app:
            self._admin_app = admin_app
        if views:
            self._views_list = views

        for view in self._views_list:
            self._admin_app.add_view(view)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role]


class ProjectAdmin(ModelView, model=Project):
    column_list = [Project.id, Project.name, Project.creator_id]


class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.title, Task.creator_id]


class TaskCommentAdmin(ModelView, model=TaskComment):
    column_list = [TaskComment.id, TaskComment.user_id, TaskComment.content]
