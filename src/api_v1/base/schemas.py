from typing import Optional

from pydantic import BaseModel


class StatusMsg(BaseModel):
    status: Optional[str] = "ok"
    detail: Optional[str] = "Success"
