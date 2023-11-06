from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.api_v1.users.views import get_user_by_id_handler, get_users_handler

router = APIRouter(prefix="/pages", tags=["Pages"])

templates = Jinja2Templates(directory="src/front/templates")


@router.get("/", response_class=HTMLResponse)
def get_base_pg(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


# @router.get("/search/{profile}/{projects}/{tasks}")
@router.get("/search", response_class=HTMLResponse)
def search_pg(request: Request, users=Depends(get_users_handler)):
    return templates.TemplateResponse("search.html", {"request": request, "users": users})


@router.get("/user/{user_id}", response_class=HTMLResponse)
def user_page(request: Request, user=Depends(get_user_by_id_handler)):
    return templates.TemplateResponse("user.html", {"request": request, "user_": user})


@router.get("/search_by_id/{user_id}", response_class=HTMLResponse)
def search_by_id_page(request: Request, user=Depends(get_user_by_id_handler)):
    return templates.TemplateResponse("user.html", {"request": request, "user_": user})
