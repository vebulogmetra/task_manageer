from datetime import datetime, timedelta
from typing import Any

import pytz
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import settings


class PwdHelper:
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid password on username",
    )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            is_pwd_valid: bool = self.pwd_context.verify(plain_password, hashed_password)
        except (ValueError, TypeError):
            raise self.http_exception
        else:
            if not is_pwd_valid:
                raise self.http_exception
            return is_pwd_valid

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)


class JWTHelper:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Bad token",
    )

    @staticmethod
    def create_token(data: dict, type: str) -> str:
        """Create jwt token. Params:
        `data` - data to encode
        `type` - access or refresh token"""
        to_encode: dict = data.copy()
        to_encode.update({"id": str(to_encode["id"])})
        expire_min: int = (
            settings.jwt_access_expire_min
            if type == "access"
            else settings.jwt_refresh_expire_min
        )

        expires = datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(
            minutes=expire_min
        )
        to_encode.update({"exp": expires})
        token: str = jwt.encode(
            claims=to_encode, key=settings.jwt_secret, algorithm=settings.jwt_algorithm
        )
        return token

    def validate_token(self, token: str) -> dict[str, Any]:
        """Validate jwt token. Params:
        `token` - accesss or refresh jwt token
        Return: The dict representation of the claims set"""
        try:
            payload: dict[str, Any] = jwt.decode(
                token=token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm]
            )
            return payload
        except JWTError:
            raise self.http_exception

    def auth_depends(self, token: str = Depends(oauth2_scheme)) -> str:
        try:
            payload = self.validate_token(token)
            username: str = payload.get("sub")
            if username is None:
                raise self.http_exception
        except JWTError:
            raise self.http_exception
        return username


pwd_helper: PwdHelper = PwdHelper()
jwt_helper: JWTHelper = JWTHelper()
