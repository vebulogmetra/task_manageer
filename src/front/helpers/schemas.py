from dataclasses import dataclass

from src.api_v1.auth.schemas import TokenUserData


@dataclass
class AuthResponse:
    is_auth_passed: bool = False
    current_user: TokenUserData | None = None
