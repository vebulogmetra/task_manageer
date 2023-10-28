from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.base.schemas import StatusMsg
from src.api_v1.users import crud
from src.api_v1.users.schemas import UserCreate, UserGet, UserUpdate
from src.core.utils.database import db_helper

router = APIRouter()


@router.post("/create", response_model=UserGet)
async def create_user_handler(
    user_data: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(db_session=session, user_data=user_data)


@router.get("/users", response_model=list[UserGet])
async def get_users_handler(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(db_session=session)


@router.get("/user/{user_id}", response_model=UserGet)
async def get_user_by_id_handler(
    user_id: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user: UserGet = await crud.get_user(db_session=session, user_id=user_id)
    return user


@router.put("/update/{user_id}", response_model=UserGet)
async def update_user_handler(
    user_id: str,
    update_data: UserUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    upd_user: UserGet = await crud.update_user(
        db_session=session, user_id=user_id, update_data=update_data
    )
    return upd_user


@router.delete("/delete/{user_id}", response_model=StatusMsg)
async def delete_user_handler(
    user_id: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    deleted_user_id: UUID | None = await crud.delete_user(
        db_session=session, user_id=user_id
    )
    return StatusMsg(detail=f"Deleted user_id: {deleted_user_id}")
