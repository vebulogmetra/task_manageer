from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import JWTToken, TokensPair
from src.api_v1.auth.service import authenticate
from src.core.utils.database import get_db

router = APIRouter()


@router.post("/login", response_model=JWTToken)
async def login_handler(
    request: Request,
    auth_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    user_host: str = request.client.host  # noqa
    user_ua: str = request.headers.get("user-agent")  # noqa

    tokens: TokensPair = await authenticate(db_session=session, auth_data=auth_data)
    response_data: JWTToken = JWTToken(
        access=tokens.access, refresh=tokens.refresh, token_type="bearer"
    )
    return response_data
