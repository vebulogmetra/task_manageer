from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import JWTToken
from src.api_v1.auth.service import authenticate
from src.api_v1.users.schemas import UserCreate
from src.api_v1.users.views import signup_user_handler
from src.core.config import html_templates, settings
from src.front.pages.auth.service import LoginForm, SignupForm
from src.utils.database import get_db

router = APIRouter(tags=["Front"])


@router.get("/signup")
def show_signup_page(request: Request):
    context = {"request": request}
    return html_templates.TemplateResponse(name="signup.html", context=context)


@router.post("/signup")
async def signup_post(request: Request, session: AsyncSession = Depends(get_db)):
    form = SignupForm(request)
    await form.load_data()
    if await form.is_valid(db_session=session):
        try:
            response = RedirectResponse(
                f"{settings.front_prefix}/", status.HTTP_302_FOUND
            )
            user_data = {
                "username": form.username,
                "email": form.email,
                "role": form.role,
                "position": form.position,
                "first_name": form.first_name,
                "last_name": form.last_name,
                "password": form.password,
            }
            user_data = UserCreate(**user_data)
            await signup_user_handler(user_data=user_data, session=session)
            return response
        except HTTPException:
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return html_templates.TemplateResponse("signup.html", form.__dict__)
    return html_templates.TemplateResponse("signup.html", form.__dict__)


@router.get("/login", response_class=HTMLResponse)
def show_login_page(request: Request):
    context = {"request": request}
    return html_templates.TemplateResponse(name="login.html", context=context)


@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, session: AsyncSession = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse(
                f"{settings.front_prefix}/", status.HTTP_302_FOUND
            )
            tokens: JWTToken = await authenticate(db_session=session, auth_data=form)
            response.set_cookie(
                key=settings.cookie_name_access,
                value=f"Bearer {tokens.access_token}",
                expires=604800,
                httponly=True,
            )
            return response
        except HTTPException:
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return html_templates.TemplateResponse("login.html", form.__dict__)
    return html_templates.TemplateResponse("login.html", form.__dict__)


@router.get("/logout", response_class=HTMLResponse)
def delete_cookie_handler():
    response = RedirectResponse(f"{settings.front_prefix}/", status.HTTP_302_FOUND)
    response.delete_cookie(key=settings.cookie_name_access)
    return response
