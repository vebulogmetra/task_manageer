import secrets
from typing import Optional
from uuid import UUID

from sqlalchemy import delete, exists, select, update
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.users.models import User, UserProfile
from src.api_v1.users.schemas import (
    UserCreate,
    UserProfileCreate,
    UserProfileUpdate,
    UserUpdate,
)
from src.utils.auth import pwd_helper
from src.utils.exceptions import custom_exc


async def check_exists_user(
    db_session: AsyncSession, by_field: str, by_value: str
) -> bool:
    stmt = select(exists().where(getattr(User, by_field) == by_value))
    user_exists = await db_session.scalar(stmt)
    return user_exists


async def signup_user(db_session: AsyncSession, user_data: UserCreate) -> User:
    user_data: dict = user_data.model_dump()
    pwd_hash: str = pwd_helper.get_password_hash(password=user_data.pop("password", None))
    user_data.update({"hashed_password": pwd_hash})
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


def after_signup_user():
    # Send verification email
    return secrets.token_hex(4)


async def create_user(db_session: AsyncSession, user_data: UserCreate) -> User:
    user_data: dict = user_data.model_dump()
    pwd_hash: str = pwd_helper.get_password_hash(password=user_data.pop("password", None))
    user_data.update({"hashed_password": pwd_hash})
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)  # Если на стороне БД генерятся данные
    return user


async def create_user_profile(
    db_session: AsyncSession, profile_data: UserProfileCreate
) -> UserProfile:
    profile_data: dict = profile_data.model_dump()
    profile = UserProfile(**profile_data)
    db_session.add(profile)
    await db_session.commit()
    return profile


async def get_users(db_session: AsyncSession) -> list[User]:
    # options = [
    #     joinedload(User.profile),
    #     selectinload(User.projects),
    #     selectinload(User.tasks),
    # ]

    stmt = select(User).order_by(User.created_at)

    result: Result = await db_session.execute(stmt)
    users: list[User] = result.scalars().all()
    if users is None:
        raise custom_exc.not_found(entity_name=User.__name__)
    return list(users)


async def get_user(db_session: AsyncSession, by_field: str, by_value: str) -> User:
    stmt = select(User).where(getattr(User, by_field) == by_value)
    try:
        user: User = await db_session.scalar(stmt)
    except NoResultFound:
        raise custom_exc.not_found(entity_name=User.__name__)
    return user


async def get_user_profile(
    db_session: AsyncSession,
    profile_id: Optional[UUID] = None,
    user_id: Optional[UUID] = None,
) -> UserProfile:
    if user_id:
        stmt = select(UserProfile).where(UserProfile.user_id == user_id)
    elif profile_id:
        stmt = select(UserProfile).where(UserProfile.id == profile_id)
    else:
        raise custom_exc.invalid_input(detail="Invalid input data")
    try:
        profile: UserProfile = await db_session.scalar(stmt)
    except NoResultFound:
        raise custom_exc.not_found(entity_name=UserProfile.__name__)
    return profile


async def get_user_by_email(db_session: AsyncSession, email: str) -> User:
    # Not used in veiws
    stmt = select(User).where(User.email == email)
    user: User | None = await db_session.scalar(stmt)
    return user


async def update_user(
    db_session: AsyncSession, user_id: UUID, update_data: UserUpdate
) -> User:
    stmt = (
        update(User)
        .returning(User)
        .where(User.id == user_id)
        .values(**update_data.model_dump())
    )

    result: Result = await db_session.execute(stmt)
    upd_user: User = result.scalar()
    await db_session.commit()
    # await db_session.refresh(upd_user)
    return upd_user


async def update_user_profile(
    db_session: AsyncSession, user_id: UUID, update_data: UserProfileUpdate
):
    upd_data: dict = update_data.model_dump()
    upd_data = [{k: v} for k, v in upd_data.items()]
    profile: UserProfile = await db_session.scalar(
        select(UserProfile).where(UserProfile.user_id == user_id)
    )
    stmt = (
        update(UserProfile)
        .where(UserProfile.id == profile.id)
        .values(**update_data.model_dump())
    )
    await db_session.execute(stmt)
    await db_session.commit()


async def delete_user(db_session: AsyncSession, user_id: UUID) -> UUID:
    stmt = delete(User).returning(User.id).where(User.id == user_id)
    result: Result = await db_session.execute(stmt)
    user_id: UUID | None = result.scalar()
    if user_id is None:
        raise custom_exc.not_found(entity_name=User.__name__)
    await db_session.commit()
    return user_id
