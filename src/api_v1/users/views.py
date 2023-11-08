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
    SignupGet,
    UserCreate,
    UserGet,
    UserProfileCreate,
    UserProfileGet,
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


@router.post("/create_profile", response_model=UserProfileGet)
async def create_profile_handler(
    profile_data: UserProfileCreate,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_user_profile(db_session=session, profile_data=profile_data)


@router.post("/upload", summary="Upload Profile picture")
async def upload_profile_image(
    user_id: str,
    picture: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
):
    mimetype = picture.content_type
    print(f"MIMETYPE: {mimetype}")
    secure_name = secure_filename(picture.filename)
    randon_hash = secrets.token_urlsafe(8)
    picture_filename = f"{secure_name}_{randon_hash}"

    with open(f"src/front/static/profileimages/{picture_filename}", "wb") as buffer:
        shutil.copyfileobj(picture.file, buffer)

    await crud.update_user_profile(
        db_session=session, user_id=user_id, update_data={"avatar_url": picture_filename}
    )

    return f"{secure_name} has been Successfully Uploaded"


@router.get("/users", response_model=list[UserGet])
async def get_users_handler(
    session: AsyncSession = Depends(get_db),
    _: TokenUserData = Depends(get_current_user),
):
    users = await crud.get_users(db_session=session)
    return users


@router.get("/get_profile", response_model=UserProfileGet)
async def get_profile_by_id_handler(
    user_id: Optional[str] = None,
    profile_id: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if user_id is None and profile_id is None:
        user_id = current_user.id
    profile: UserProfileGet = await crud.get_user_profile(
        db_session=session, profile_id=profile_id, user_id=user_id
    )
    return profile


@router.get("/user", response_model=UserGet)
async def get_user_handler(
    by_value: Optional[str] = None,
    by_field: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if by_value is None or by_field is None:
        by_field = "id"
        by_value = current_user.id
    user: UserGet = await crud.get_user(
        db_session=session, by_field=by_field, by_value=by_value
    )
    return user


@router.put("/update/{user_id}", response_model=UserGet)
async def update_user_handler(
    user_id: str,
    update_data: UserUpdate,
    session: AsyncSession = Depends(get_db),
):
    upd_user: UserGet = await crud.update_user(
        db_session=session, user_id=user_id, update_data=update_data
    )
    return upd_user


@router.delete("/delete/{user_id}", response_model=StatusMsg)
async def delete_user_handler(
    user_id: str,
    session: AsyncSession = Depends(get_db),
):
    deleted_user_id: UUID | None = await crud.delete_user(
        db_session=session, user_id=user_id
    )
    return StatusMsg(detail=f"Deleted user_id: {deleted_user_id}")
