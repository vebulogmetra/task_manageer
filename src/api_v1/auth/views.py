from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.google.views import router as google_auth_router
from src.api_v1.auth.schemas import JWTToken
from src.api_v1.auth.service import authenticate
from src.utils.database import get_db

router = APIRouter()
router.include_router(router=google_auth_router, prefix="/google")


@router.post("/login", response_model=JWTToken)
async def login_handler(
    request: Request,
    auth_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    """Обмен email и password на JWTToken: access_token, refresh_token, token_type"""
    user_host: str = request.client.host  # noqa
    user_ua: str = request.headers.get("user-agent")  # noqa

    tokens: JWTToken = await authenticate(db_session=session, auth_data=auth_data)
    return tokens
