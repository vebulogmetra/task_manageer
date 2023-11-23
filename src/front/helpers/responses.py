from fastapi import status
from fastapi.responses import RedirectResponse

from src.core.config import settings

redirect_to_login: RedirectResponse = RedirectResponse(
    url=f"{settings.front_prefix}/login", status_code=status.HTTP_302_FOUND
)
