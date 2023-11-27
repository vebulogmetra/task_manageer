import secrets
from urllib.parse import urlencode

import requests
from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from google.auth.exceptions import MalformedError
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token
from pydantic_core import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import GoogleUserinfo, JWTToken, TokenUserData
from src.api_v1.auth.service import create_tokens
from src.api_v1.users.crud import create_user, get_user_by_email
from src.api_v1.users.models import User
from src.api_v1.users.schemas import UserCreate
from src.core.config import logger, settings
from src.utils.database import get_db
from src.utils.exceptions import custom_exc

router = APIRouter()


@router.get("/login")
async def login_with_google_handler():
    """Редирект пользователя на страницу аутентификации Google"""
    # Формирование URL для аутентификации через Google
    params = {
        "response_type": "code",
        "client_id": settings.google_auth_client_id,
        "redirect_uri": settings.google_auth_redirect_url,
        "scope": " ".join(settings.google_auth_scopes),
    }
    auth_url = settings.google_auth_base_url + "?" + urlencode(params)
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def google_auth_callback(
    code: str,
    session: AsyncSession = Depends(get_db),
):
    """Обмен полученного от google кода авторизации на id_token
    в котором содержится информация о пользователе и его аутентификация"""
    # Обрабатываем коллбэк от Google и обмениваем код авторизации на id_token
    params: dict = {
        "code": code,
        "client_id": settings.google_auth_client_id,
        "client_secret": settings.google_auth_client_secret,
        "redirect_uri": settings.google_auth_redirect_url,
        "grant_type": settings.google_auth_grant_type,
    }
    token_response: requests.Response = requests.post(
        settings.google_auth_get_id_token_url, data=params
    )
    token_response: dict = token_response.json()
    if "error" in token_response:
        logger.error(f"GOOGLE_TOKEN_RESPONSE_ERROR: {token_response}")
        raise custom_exc.unauthorized(detail=f"{token_response}")
    # Проверяем и распаковываем id_token с помощью библиотеки google-auth
    try:
        id_info: dict = id_token.verify_oauth2_token(
            id_token=token_response["id_token"],
            request=GoogleRequest(),
            audience=settings.google_auth_client_id,
        )
    except MalformedError as e:
        logger.error(f"GOOGLE_ID_TOKEN_VERIFY_ERROR: {e}")
        raise custom_exc.unauthorized(detail="Invalid google authenticate")

    # Парсим данные о пользователе в модель (валидируем)
    try:
        user_info = GoogleUserinfo.model_validate(id_info)
    except ValidationError as e:
        logger.error(f"GOOGLE_USERINFO_VALIDATION_ERROR: {e}")
        raise custom_exc.internal_error(detail="Internal error")

    # Проверяем, существует ли пользователь с таким email
    user: User | None = await get_user_by_email(db_session=session, email=user_info.email)
    # Если пользователь существует, выдаём ему JWT токены (аутинефицируем)
    if user:
        tokens: JWTToken = create_tokens(
            user_data=TokenUserData(id=user.id, email=user.email)
        )
    else:
        password = secrets.token_urlsafe(8)
        # Если пользователь новый, создаём его в базе данных и выдаём JWT токены
        user = await create_user(
            db_session=session,
            user_data=UserCreate(
                username=str(user_info.sub),
                email=user_info.email,
                password=password,
                first_name=user_info.given_name,
                last_name=user_info.family_name,
            ),
        )
        logger.info(
            f"CREATE NEW USER WITH GOOGLE: USERNAME={user_info.sub} PASSWORD={password}"
        )
        tokens: JWTToken = create_tokens(
            user_data=TokenUserData(id=user.id, email=user.email)
        )

    query_response = RedirectResponse(f"{settings.front_prefix}/", status.HTTP_302_FOUND)
    query_response.set_cookie(
        key=settings.cookie_name_access,
        value=f"Bearer {tokens.access_token}",
        expires=604800,
        httponly=True,
    )
    return query_response
