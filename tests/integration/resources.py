import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from pydantic import EmailStr

from src.core.config import settings

base_api_url = settings.api_v1_prefix


@dataclass
class User:
    username: str
    email: EmailStr
    password: str
    id: str = None

    def to_dict(self):
        return asdict(self)


@dataclass
class Project:
    name: str
    description: str
    creator_id: str = None
    id: str = None

    def to_dict(self):
        return asdict(self)


@dataclass
class Task:
    title: str
    description: str
    status: str
    priority: str
    due_date: str
    project_id: str = None
    creator_id: str = None
    id: str = None

    def to_dict(self):
        return asdict(self)


@dataclass
class Team:
    title: str
    description: str
    creator_id: str = None
    id: str = None

    def to_dict(self):
        return asdict(self)


class Endpoint:
    # User
    user_create: str = os.path.join(base_api_url, "users/create")
    user_get: str = os.path.join(base_api_url, "users/user")
    users_get: str = os.path.join(base_api_url, "users/users")
    user_upload_picture: str = os.path.join(base_api_url, "users/upload_picture")
    user_update: str = os.path.join(base_api_url, "users/update")
    user_delete: str = os.path.join(base_api_url, "users/delete")
    # Project
    project_create: str = os.path.join(base_api_url, "projects/create")
    project_add_user: str = os.path.join(base_api_url, "projects/add_user")
    project_get: str = os.path.join(base_api_url, "projects/project")
    projects_get_by_owner: str = os.path.join(base_api_url, "projects/projects_by_owner")
    projects_get: str = os.path.join(base_api_url, "projects/projects")
    project_update: str = os.path.join(base_api_url, "projects/update")
    project_delete: str = os.path.join(base_api_url, "projects/delete")
    # Task
    task_create: str = os.path.join(base_api_url, "tasks/create")
    task_add_user: str = os.path.join(base_api_url, "tasks/add_user")
    task_add_comment: str = os.path.join(base_api_url, "tasks/add_comment")
    task_get: str = os.path.join(base_api_url, "tasks/task")
    tasks_get_by_owner: str = os.path.join(base_api_url, "tasks/tasks_by_owner")
    tasks_get: str = os.path.join(base_api_url, "tasks/tasks")
    task_update: str = os.path.join(base_api_url, "tasks/update")
    task_delete: str = os.path.join(base_api_url, "tasks/delete")
    # Team
    team_create: str = os.path.join(base_api_url, "teams/create")
    team_add_user: str = os.path.join(base_api_url, "teams/add_user")
    team_get: str = os.path.join(base_api_url, "teams/team")
    teams_get: str = os.path.join(base_api_url, "teams/teams")
    team_update: str = os.path.join(base_api_url, "teams/update")
    team_delete: str = os.path.join(base_api_url, "teams/delete")


class HttpStatus:
    success = 200
    notfound = 404
    unauthorized = 401
    invalid_input = 422


class Constant:
    # User
    user_login_require_fields = ("access_token", "refresh_token", "token_type")
    user_login_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    current_file = Path(__file__).resolve()
    current_dir = Path(__file__).parent
    test_image_filepath = os.path.join(
        current_dir.parent.parent, "src/front/static/profileimages", "default.png"
    )
    # Project
    project_create_response_required_fields = (
        "id",
        "name",
        "description",
        "creator_id",
        "users",
        "created_at",
        "updated_at",
    )


test_user = User(
    **{
        "username": "fedor",
        "email": "f@f.f",
        "password": "qwerty",
    }
)
test_user_developer = User(
    **{
        "username": "oleg",
        "email": "o@o.o",
        "password": "qwerty123",
    }
)
test_project = Project(
    **{"name": "myprj", "description": "very nice project"},
)
test_task = Task(
    **{
        "title": "mytask",
        "description": "very important task",
        "status": "created",
        "priority": "low",
        "due_date": datetime.now().replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S"),
    }
)
test_team = Team(**{"title": "Dream team", "description": "Your dream team"})

test_api = Endpoint()
test_status = HttpStatus()
test_const = Constant()
