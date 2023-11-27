import urllib.parse

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.core.config import settings
from src.utils.exceptions import custom_exc


class PwdHelper:
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            is_pwd_valid: bool = self.pwd_context.verify(plain_password, hashed_password)
        except (ValueError, TypeError):
            raise custom_exc.unauthorized(detail="Invalid password on username")
        else:
            if not is_pwd_valid:
                raise custom_exc.unauthorized(detail="Invalid password on username")
            return is_pwd_valid

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)


pwd_helper: PwdHelper = PwdHelper()

# By email auth backend
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=urllib.parse.urljoin(f"{settings.api_v1_prefix}/", "auth/login")
)
