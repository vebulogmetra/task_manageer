import re
import urllib.parse
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.users.crud import check_exists_user
from src.api_v1.users.schemas import AdminPositions
from src.core.config import logger, settings
from src.utils.exceptions import custom_exc


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(settings.cookie_name_access)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("A valid email is required")
        if not self.password or not len(self.password) >= 3:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


class SignupForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []

        self.username: Optional[str] = None
        self.email: Optional[str] = None
        self.first_name: Optional[str] = None
        self.last_name: Optional[str] = None
        self.position: Optional[str] = None
        self.role: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username").lower()
        self.email = form.get("email").lower()
        self.first_name = form.get("first_name").capitalize()
        self.last_name = form.get("last_name").capitalize()
        self.position = form.get("position").lower()
        self.role = self.select_user_role()
        self.password = form.get("password")

    def slugify(self, string: str) -> str:
        slugify_str = re.sub(r"\s+|\(|\)", "_", string)
        slugify_str = re.sub(r"\W+", "", slugify_str)
        if not re.match(r"^[a-zA-Z_]", slugify_str):
            slugify_str = "_" + slugify_str
        return slugify_str

    def select_user_role(self) -> str:
        self.position = self.slugify(string=self.position)
        if self.position in list(
            map(lambda x: x.value, AdminPositions._member_map_.values())
        ):
            return "admin"
        else:
            return "user"

    async def is_valid(self, db_session: AsyncSession):
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("A valid email is required")
        if not self.password or not len(self.password) >= 3:
            self.errors.append("Password is required and must be > 3 chars")
        if not self.first_name or not self.first_name.isalpha():
            self.errors.append("First name is required and can contain only letters")
        if not self.last_name or not self.first_name.isalpha():
            self.errors.append("Last name is required and can contain only letters")
        if await check_exists_user(
            db_session=db_session,
            by_field="email",
            by_value=self.email,
        ):
            self.errors.append("This email address is already registered")
        if await check_exists_user(
            db_session=db_session,
            by_field="username",
            by_value=self.username,
        ):
            self.errors.append("This username is already registered")

        if not self.errors:
            return True
        return False


def get_current_user_from_cookie(request: Request) -> TokenUserData:
    try:
        token: str = request.cookies.get(settings.cookie_name_access).split(" ")[1]
        payload = jwt.decode(
            token=token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
    except JWTError:
        logger.warning(f"Bad token '{token}'")
        return None
    except AttributeError:
        raise custom_exc.empty_auth_cookie()
    user_data = payload.get("user")
    try:
        user: TokenUserData = TokenUserData.model_validate(user_data)
    except ValidationError:
        raise custom_exc.unauthorized(detail="Bad token data")
    return user


oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl=urllib.parse.urljoin(f"{settings.api_v1_prefix}/", "auth/login")
)
