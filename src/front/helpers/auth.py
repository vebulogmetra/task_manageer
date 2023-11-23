from fastapi import Request

from src.api_v1.auth.schemas import TokenUserData
from src.front.helpers.schemas import AuthResponse
from src.front.pages.auth.service import get_current_user_from_cookie
from src.utils.exceptions import EmptyAuthCookie


def check_login(request: Request) -> AuthResponse:
    response: AuthResponse = AuthResponse()
    try:
        current_user: TokenUserData | None = get_current_user_from_cookie(request)
    except EmptyAuthCookie:
        current_user = None
    else:
        response.is_auth_passed = True
        response.current_user = current_user
    return response
