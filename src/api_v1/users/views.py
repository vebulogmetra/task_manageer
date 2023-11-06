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
from src.api_v1.users.models import ProfileImage
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
    profile_id: str, session: AsyncSession = Depends(get_db), file: UploadFile = File(...)
):
    with open(f"src/front/static/profileimages/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    name = secure_filename(file.filename)
    mimetype = file.content_type

    image_upload = ProfileImage(
        img=f"src/front/static/profileimages/{file.filename}",
        minetype=mimetype,
        name=name,
        profile_id=profile_id,
    )
    session.add(image_upload)
    await session.commit()
    return f"{name} has been Successfully Uploaded"


@router.get("/users", response_model=list[UserGet])
async def get_users_handler(
    session: AsyncSession = Depends(get_db),
    user_data: TokenUserData = Depends(get_current_user),
):
    users = await crud.get_users(db_session=session)
    return users


@router.get("/get_profile/{profile_id}", response_model=UserProfileGet)
async def get_profile_by_id_handler(
    profile_id: str,
    session: AsyncSession = Depends(get_db),
):
    profile: UserProfileGet = await crud.get_user_profile(
        db_session=session, profile_id=profile_id
    )
    return profile


@router.get("/user", response_model=UserGet)
async def get_user_by_id_handler(
    user_id: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
    user_data: TokenUserData = Depends(get_current_user),
):
    if user_id is None:
        user_id = user_data.id
    user: UserGet = await crud.get_user(db_session=session, user_id=user_id)
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
