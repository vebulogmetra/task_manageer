from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

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


@router.get("/users", response_model=list[UserGet])
async def get_users_handler(
    profile: Optional[bool] = False,
    projects: Optional[bool] = False,
    tasks: Optional[bool] = False,
    session: AsyncSession = Depends(get_db),
):
    users = await crud.get_users(
        db_session=session, profile=profile, projects=projects, tasks=tasks
    )
    return users


@router.get("/user/{user_id}", response_model=UserGet)
async def get_user_by_id_handler(
    user_id: str,
    profile: Optional[bool] = False,
    projects: Optional[bool] = False,
    tasks: Optional[bool] = False,
    session: AsyncSession = Depends(get_db),
):
    user: UserGet = await crud.get_user(
        db_session=session,
        user_id=user_id,
        profile=profile,
        projects=projects,
        tasks=tasks,
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
