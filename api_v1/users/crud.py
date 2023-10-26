from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserCreate
from src.core.models.user import User


async def get_users(db_session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.created_at)
    result: Result = await db_session.execute(stmt)
    users: list[User] = result.scalars().all()
    return list(users)


async def get_user(db_session: AsyncSession, user_id: UUID) -> User | None:
    return await db_session.get(User, user_id)


async def create_user(db_session: AsyncSession, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)  # Если на стороне БД генертся данные
    return user
