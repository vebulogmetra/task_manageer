from uuid import UUID

from pydantic import BaseModel, EmailStr


class JWTToken(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str = "bearer"


class TokenUserData(BaseModel):
    id: UUID
    email: EmailStr


class GoogleUserinfo(BaseModel):
    iss: str
    azp: str
    aud: str
    sub: int
    email: EmailStr
    email_verified: bool
    at_hash: str
    name: str
    picture: str
    given_name: str
    family_name: str
    locale: str
    iat: int
    exp: int
