import os
from dataclasses import asdict, dataclass
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
    project_upload_picture: str = os.path.join(base_api_url, "projects/upload_picture")
    project_update: str = os.path.join(base_api_url, "projects/update")
    project_delete: str = os.path.join(base_api_url, "projects/delete")


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


test_user = User(**{"username": "fedor", "email": "f@f.f", "password": "qwerty"})
test_user_developer = User(
    **{"username": "oleg", "email": "o@o.o", "password": "qwerty123"}
)
test_project = Project(**{"name": "myprj", "description": "very nice project"})
test_api = Endpoint()
test_status = HttpStatus()
test_const = Constant()
