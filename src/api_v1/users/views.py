import secrets
import shutil
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
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
from src.utils.database import get_db

router = APIRouter()


@router.post("/signup", response_model=SignupGet)
async def signup_user_handler(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
):
    user_data.role = user_data.role.value
    new_user: UserGet = await crud.signup_user(db_session=session, user_data=user_data)
    verif_code: str = crud.after_signup_user()
    return {"verif_code": verif_code, "new_user": new_user}


@router.post("/create", response_model=UserGet)
async def create_user_handler(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
):
    user_data.role = user_data.role.value
    return await crud.create_user(db_session=session, user_data=user_data)


@router.post(
    "/upload_picture", summary="Upload Profile picture", response_model=StatusMsg
)
async def upload_avatar_picture(
    user_id: Optional[str] = None,
    picture: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    # :TODO Resize images
    if user_id is None:
        user_id = current_user.id

    # if picture.content_type == "image/jpeg"

    secure_name = secure_filename(picture.filename)
    name, ext = secure_name.split(".")
    randon_hash = secrets.token_urlsafe(8)
    picture_filename = f"{name}_{randon_hash}.{ext}"
    # :TODO Replace to settings root path
    with open(f"src/front/static/profileimages/{picture_filename}", "wb") as buffer:
        shutil.copyfileobj(picture.file, buffer)

    await crud.update_user(
        db_session=session,
        user_id=user_id,
        update_data=UserUpdate(avatar_url=picture_filename),
    )

    return StatusMsg(status="ok", detail=f"{secure_name} has been Successfully Uploaded")


# @router.get("/users", response_model=list[UserGet])
@router.get("/users")
async def get_users_handler(
    session: AsyncSession = Depends(get_db),
    _: TokenUserData = Depends(get_current_user),
):
    users = await crud.get_users(db_session=session)
    return users


@router.get("/user", response_model=UserGet)
async def get_user_handler(
    by_value: Optional[str] = None,
    by_field: Optional[GetUserFields] = None,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if by_value is None:
        by_field = GetUserFields.id.value
        by_value = current_user.id

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
