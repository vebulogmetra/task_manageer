import os
import secrets
import shutil
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.utils import secure_filename

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.auth.service import get_current_user
from src.api_v1.base.schemas import StatusMsg
from src.api_v1.users import crud
from src.api_v1.users.schemas import (
    GetUserFields,
    SignupGet,
    UserCreate,
    UserGet,
    UserUpdate,
)
from src.core.config import settings
from src.utils.database import get_db

router = APIRouter()


@router.post("/signup", response_model=SignupGet)
async def signup_user_handler(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
):
    new_user: UserGet = await crud.signup_user(db_session=session, user_data=user_data)
    verif_code: str = crud.after_signup_user()
    return {"verif_code": verif_code, "new_user": new_user}


@router.post("/create", response_model=UserGet)
async def create_user_handler(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_user(db_session=session, user_data=user_data)


@router.post(
    "/upload_picture",
    summary="Upload Profile picture",
    response_model=StatusMsg,
)
async def upload_avatar_picture(
    user_id: str = Form(...),
    picture: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
    # current_user: TokenUserData = Depends(get_current_user),
):
    # :TODO Resize images
    # :TODO if picture.content_type == "image/jpeg"

    secure_name: str = secure_filename(picture.filename)
    name, ext = secure_name.split(".")
    random_hash: str = secrets.token_urlsafe(8)
    picture_filename: str = f"{name}_{random_hash}.{ext}"
    with open(
        os.path.join(settings.html_staticfiles_path, "profileimages", picture_filename),
        "wb",
    ) as buffer:
        shutil.copyfileobj(picture.file, buffer)

    await crud.update_user(
        db_session=session,
        user_id=user_id,
        update_data=UserUpdate(avatar_url=picture_filename),
    )
    response = StatusMsg(
        status="ok", detail=f"{secure_name} has been Successfully Uploaded"
    )
    return response


@router.get("/total_users")
async def get_total_users_count_handler(session: AsyncSession = Depends(get_db)):
    total_users: int = await crud.get_total_users(db_session=session)
    return total_users


@router.get("/users", response_model=list[UserGet])
async def get_users_handler(
    session: AsyncSession = Depends(get_db),
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    _: TokenUserData = Depends(get_current_user),
):
    users = await crud.get_users(db_session=session, limit=limit, offset=offset)
    return users


@router.get("/user", response_model=UserGet)
async def get_user_handler(
    by_value: Optional[str] = None,
    by_field: Optional[GetUserFields] = None,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if by_value is None:
        by_field = GetUserFields.id
        by_value = str(current_user.id)

    user: UserGet = await crud.get_user(
        db_session=session, by_field=by_field.value, by_value=by_value
    )
    return user


@router.put("/update", response_model=UserGet)
async def update_user_handler(
    update_data: UserUpdate,
    user_id: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if user_id is None:
        user_id = current_user.id
    upd_user: UserGet = await crud.update_user(
        db_session=session, user_id=user_id, update_data=update_data
    )
    return upd_user


@router.delete("/delete", response_model=StatusMsg)
async def delete_user_handler(
    user_id: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if user_id is None:
        user_id = current_user.id
    deleted_user_id: UUID | None = await crud.delete_user(
        db_session=session, user_id=user_id
    )
    return StatusMsg(detail=f"Deleted user_id: {deleted_user_id}")
