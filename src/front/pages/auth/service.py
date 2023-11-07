import urllib.parse
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from pydantic import ValidationError

from src.api_v1.auth.schemas import TokenUserData
from src.core.config import settings
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
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 2:
            self.errors.append("A valid password is required")
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
        raise custom_exc.unauthorized(detail="Bad token")
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