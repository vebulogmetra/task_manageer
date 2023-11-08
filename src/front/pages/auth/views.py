from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import JWTToken
from src.api_v1.auth.service import authenticate
from src.core.config import settings
from src.front.pages.auth.service import LoginForm
from src.utils.database import get_db

templates = Jinja2Templates(directory="src/front/templates")

router = APIRouter(tags=["Front"])


@router.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, session: AsyncSession = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse(
                f"{settings.front_prefix}/", status.HTTP_302_FOUND
            )
            await login_for_access_token(
                response=response, auth_data=form, session=session
            )
            form.__dict__.update(msg="Login Successful!")
            print("Login successful!!!!")
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)


@router.get("/logout", response_class=HTMLResponse)
def logout_page():
    response = RedirectResponse(f"{settings.front_prefix}/", status.HTTP_302_FOUND)
    response.delete_cookie(key=settings.cookie_name_access)
    return response


@router.post("/token")
async def login_for_access_token(
    response: Response,
    session,
    auth_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    tokens: JWTToken = await authenticate(db_session=session, auth_data=auth_data)
    # Set an HttpOnly cookie in the response. `httponly=True` prevents
    # JavaScript from reading the cookie.
    response.set_cookie(
        key=settings.cookie_name_access,
        value=f"Bearer {tokens.access_token}",
        httponly=True,
    )
    response.set_cookie(
        key=f"Refresh_{settings.cookie_name_access}",
        value=f"Bearer {tokens.refresh_token}",
        httponly=True,
    )
    return {settings.cookie_name_access: tokens.access_token, "token_type": "bearer"}