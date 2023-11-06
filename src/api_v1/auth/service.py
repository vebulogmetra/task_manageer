from datetime import datetime, timedelta
from uuid import UUID

import pytz
from fastapi import Security
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import JWTToken, TokenUserData
from src.api_v1.users import crud as user_crud
from src.api_v1.users.models import User
from src.core.config import settings
from src.utils.auth import oauth2_scheme, pwd_helper
from src.utils.exceptions import custom_exc


def uuid_values_formatter(dict_: dict) -> dict:
    for k, v in dict_.items():
        if isinstance(v, UUID):
            dict_[k] = str(v)
    return dict_


def create_tokens(user_data: TokenUserData) -> JWTToken:
    now = datetime.now(pytz.timezone("Europe/Moscow"))
    user_data: dict = uuid_values_formatter(dict_=user_data.model_dump())

    payload = {
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=settings.jwt_access_expire_min),
        "sub": str(user_data.get("email", None)),
        "user": user_data,
    }
    try:
        access_token: str = jwt.encode(
            claims=payload,
            key=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        payload["exp"] = now + timedelta(minutes=settings.jwt_refresh_expire_min)
        refresh_token: str = jwt.encode(
            claims=payload,
            key=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
    except Exception as err:
        print(f"Jwt encode error:\n{err}")
        raise custom_exc.internal_error(detail="Jwt encode error")
    return JWTToken(access_token=access_token, refresh_token=refresh_token)


async def authenticate(
    db_session: AsyncSession, auth_data: OAuth2PasswordRequestForm
) -> JWTToken:
    email: str = auth_data.username
    password: str = auth_data.password

    user_exists: bool = await user_crud.check_exists_user(
        db_session=db_session, by_field="email", by_value=email
    )
    if not user_exists:
        raise custom_exc.unauthorized(detail="Invalid email")

    user: User = await user_crud.get_user_by_email(db_session=db_session, email=email)
    if user is None:
        raise custom_exc.not_found(entity_name="User")

    pwd_helper.verify_password(
        plain_password=password, hashed_password=user.hashed_password
    )

    tokens: JWTToken = create_tokens(
        user_data=TokenUserData(id=user.id, email=user.email)
    )
    return tokens


def get_current_user(token: str = Security(oauth2_scheme)) -> TokenUserData:
    try:
        payload = jwt.decode(
            token=token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
    except JWTError:
        raise custom_exc.unauthorized(detail="Bad token")
    user_data = payload.get("user")
    try:
        user: TokenUserData = TokenUserData.model_validate(user_data)
    except ValidationError:
        raise custom_exc.unauthorized(detail="Bad token data")
    return user
