from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import JWTToken
from src.api_v1.auth.service import authenticate
from src.api_v1.users.schemas import UserCreate
from src.api_v1.users.views import signup_user_handler
from src.core.config import settings
from src.front.pages.auth.service import LoginForm, SignupForm
from src.utils.database import get_db

templates = Jinja2Templates(directory="src/front/templates")

router = APIRouter(tags=["Front"])


@router.get("/signup")
def signup_page(request: Request):
    ctx = {"request": request}
    return templates.TemplateResponse(name="signup.html", context=ctx)


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
            return templates.TemplateResponse("signup.html", form.__dict__)
    return templates.TemplateResponse("signup.html", form.__dict__)


@router.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    ctx = {"request": request}
    return templates.TemplateResponse(name="login.html", context=ctx)


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
            return response
        except HTTPException:
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
        expires=604800,
        httponly=True,
    )
    return {settings.cookie_name_access: tokens.access_token, "token_type": "bearer"}


#########################################

from authlib.integrations.starlette_client import OAuth, OAuthError

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.google_auth_client_id,
    client_secret=settings.google_auth_client_secret,
    client_kwargs={
        "scope": "email openid profile",
        "redirect_url": settings.google_auth_redirect_url,
    },
)


@router.get("/google_login")
async def login_with_google(request: Request):
    return await oauth.google.authorize_redirect(
        request, settings.google_auth_redirect_url
    )


# http://127.0.0.1:8000/front/pages/google_callback
@router.get("/google_callback")
async def google_auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)

        print(f"GOOGLE ACCESS TOKEN: {token}")

        # {
        # "access_token":"ya29.a0AfB_byCL2D5gDOhIfbkDaDwq6tnj08Yv1eKJUKvaxIvIxQ2Wr8RNSCW2VrjzVvVUmF-qkDig_Rz2WuKfStjP47uC-hTvq1uiL0dhkdr3WT0k-wpcOzKe9IV7ZY5fkdXLtPEcq4ADr6MDJ26qLs1jlg3vXMpwDMzRAf5maCgYKAYgSARMSFQHGX2Mi_RpAYBf8sOo6-B8D1Lfv7g0171",
        # "expires_in":3599,
        # "scope":"https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
        # "token_type":"Bearer",
        # "id_token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjBlNzJkYTFkZjUwMWNhNmY3NTZiZjEwM2ZkN2M3MjAyOTQ3NzI1MDYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDg4MTk2MDEwNzczLWRiNmF1dDNhYm9udXRtYm1sc3Q4MmpidDJldWIybTY0LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTA4ODE5NjAxMDc3My1kYjZhdXQzYWJvbnV0bWJtbHN0ODJqYnQyZXViMm02NC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExNjMzODIzMzc0NTQyMTQ5NDY5NiIsImVtYWlsIjoic2VsaXZhbmZlZG9yQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiUkdGRS1XbW13bFN2Q1lkS2c0VVFEUSIsIm5vbmNlIjoiU1VTNHAzdmd2TW12V21USUx2aUYiLCJuYW1lIjoi0JjQs9C90LDRgiDQltC10LvQtdC30L3QvtCyIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0szMGFXSW9hUnpfTWNRekp0UUZyN3pyOFh6cWlTbDNrSUpZNXlyQ3lOei1Qcz1zOTYtYyIsImdpdmVuX25hbWUiOiLQmNCz0L3QsNGCIiwiZmFtaWx5X25hbWUiOiLQltC10LvQtdC30L3QvtCyIiwibG9jYWxlIjoicnUiLCJpYXQiOjE3MDA4NTY2NDgsImV4cCI6MTcwMDg2MDI0OH0.UeMXbWhs_TYrF2ygR6s4hLlmiW5FYtnQW40n1lujRlk0RoX_u2fkJ9Ox7OCSHi-tJjidttukgcVhzdKWujPz239lTDbyWQosNqfqsUzl0s1U5mV7dWitu3maMA8_z7jUpk1QGa1GVuPhm2X1cNlx0ekASCzAOItef8XxARoh401zWF9tJuUDdpldvVMtSohnQrDo_qgvbULie9hKcDQNIayBi38x4A7J5_5aRuSjU8vB918q2oSI3xOwRrJYT5kUxky_P7WkVR-1Dhh5M5gFi7f_gWCxkWotAo9eNdNG7rFcFDRvjnTFYJ9Uk89V5zZ4SUN0Na8spZ97o4b-qB1L7Q",
        # "expires_at":1700860247
        # }

    except OAuthError as e:
        return templates.TemplateResponse(
            name="error.html", context={"request": request, "error": e.error}
        )
    user = token.get("userinfo")

    print(f"GOOGLE USER INFO: {user}")

    # {
    # "iss":"https://accounts.google.com",
    # "azp":"1088196010773-db6aut3abonutmbmlst82jbt2eub2m64.apps.googleusercontent.com",
    # "aud":"1088196010773-db6aut3abonutmbmlst82jbt2eub2m64.apps.googleusercontent.com",
    # "sub":"116338233745421494696",
    # "email":"selivanfedor@gmail.com",
    # "email_verified":true,
    # "at_hash":"RGFE-WmmwlSvCYdKg4UQDQ",
    # "nonce":"SUS4p3vgvMmvWmTILviF",
    # "name":"Игнат Железнов",
    # "picture":"https://lh3.googleusercontent.com/a/ACg8ocK30aWIoaRz_McQzJtQFr7zr8XzqiSl3kIJY5yrCyNz-Ps=s96-c",
    # "given_name":"Игнат",
    # "family_name":"Железнов",
    # "locale":"ru",
    # "iat":1700856648,
    # "exp": 1700856648
    # }

    if user:
        request.session["user"] = dict(user)
    return RedirectResponse(f"{settings.front_prefix}/", status.HTTP_302_FOUND)


@router.post("/google_logout")
async def logout_google(request: Request):
    request.session.pop("user", None)
    return RedirectResponse("/")


def login_required(func):
    def wrapper(*args, session, **kwargs):
        if "google_id" in session:
            print("GOOGLE_ID not in session!")
            return False
        else:
            return func

    return wrapper


@router.post("/google_protected")
@login_required
async def google_protected(request: Request):
    pass
