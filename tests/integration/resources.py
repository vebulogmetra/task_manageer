import os
from dataclasses import asdict, dataclass

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


class Endpoint:
    user_create: str = os.path.join(base_api_url, "users/create")
    user_get: str = os.path.join(base_api_url, "users/user")
    users_get: str = os.path.join(base_api_url, "users/users")


class HttpStatus:
    success = 200


class Constant:
    user_login_require_fields = ("access_token", "refresh_token", "token_type")
    user_login_headers = {"Content-Type": "application/x-www-form-urlencoded"}


test_user = User(**{"username": "fedor", "email": "f@f.f", "password": "qwerty"})
test_api = Endpoint()
test_status = HttpStatus()
test_const = Constant()
