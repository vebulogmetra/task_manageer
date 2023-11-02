from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class WithUser(BaseModel):
    id: UUID
    username: str
    email: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
