from typing import NamedTuple

from pydantic import BaseModel


class JWTToken(BaseModel):
    access: str
    refresh: str
    type: str = "bearer"


class TokensPair(NamedTuple):
    access: str
    refresh: str
