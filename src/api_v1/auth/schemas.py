from uuid import UUID

from pydantic import BaseModel, EmailStr


class JWTToken(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str = "bearer"


class TokenUserData(BaseModel):
    id: UUID
    email: EmailStr
