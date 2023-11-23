from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.core.config import settings
from src.front.helpers import auth as auth_helper
from src.front.helpers.responses import redirect_to_login
from src.front.helpers.schemas import AuthResponse

router = APIRouter()

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/", response_class=HTMLResponse)
def get_index_page(request: Request):
    response: RedirectResponse = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed:
        response = RedirectResponse(
            url=f"{settings.front_prefix}/account", status_code=status.HTTP_302_FOUND
        )
    return response


@router.get("/home", response_class=HTMLResponse)
def get_home_page(request: Request):
    response = redirect_to_login
    auth_data: AuthResponse = auth_helper.check_login(request=request)
    if auth_data.is_auth_passed and auth_data.current_user:
        context = {
            "logged_in": auth_data.is_auth_passed,
            "user": auth_data.current_user,
            "request": request,
        }
        response = templates.TemplateResponse("home.html", context)
    return response
