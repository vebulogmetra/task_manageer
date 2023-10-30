from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.base.exceptions import custom_exc
from src.api_v1.users.schemas import UserCreate, UserUpdate
from src.core.models.user import User
from src.core.utils.auth import pwd_hepler


async def create_user(db_session: AsyncSession, user_data: UserCreate) -> User:
    user_data: dict = user_data.model_dump()
    pwd_hash: str = pwd_hepler.get_password_hash(password=user_data.pop("password", None))
    user_data.update({"hashed_password": pwd_hash})
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)  # Если на стороне БД генерятся данные
    return user


async def get_users(db_session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.created_at)
    result: Result = await db_session.execute(stmt)
    users: list[User] = result.scalars().all()
    if users is None:
        raise custom_exc.generate_exception(entity_name=User.__name__)
    return list(users)


async def get_user(db_session: AsyncSession, user_id: UUID) -> User:
    try:
        user: User = await db_session.get(User, user_id)
    except NoResultFound:
        raise custom_exc.generate_exception(entity_name=User.__name__)
    return user


async def update_user(db_session: AsyncSession, user_id: UUID, update_data: UserUpdate) -> User:
    stmt = update(User).returning(User).where(User.id == user_id).values(**update_data.model_dump())

    result: Result = await db_session.execute(stmt)
    upd_user: User = result.scalar()
    await db_session.commit()
    # await db_session.refresh(upd_user)
    return upd_user


async def delete_user(db_session: AsyncSession, user_id: UUID) -> UUID:
    stmt = delete(User).returning(User.id).where(User.id == user_id)
    result: Result = await db_session.execute(stmt)
    user_id: UUID | None = result.scalar()
    if user_id is None:
        raise custom_exc.generate_exception(entity_name=User.__name__)
    await db_session.commit()
    return user_id
