from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.users import crud
from src.api_v1.users.schemas import UserCreate, UserGet
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


@router.get("/user/{user_id}/", response_model=UserGet)
async def get_user_by_id_handler(
    user_id: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = crud.get_user(db_session=session, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )


@router.put("/update/{user_id}/")
async def update_user_handler(
    updated_data: dict,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    pass


@router.delete("/delete/{user_id}/")
async def delete_user_handler(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    pass
