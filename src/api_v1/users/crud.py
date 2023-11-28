import secrets
from pathlib import Path
from uuid import UUID

from sqlalchemy import delete, exists, func, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.base.utils import is_valid_uuid
from src.api_v1.users.models import User
from src.api_v1.users.schemas import GetUserFields, UserCreate, UserUpdate
from src.core.config import settings
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
    if not isinstance(user_data.get("position"), str):
        user_data["position"] = user_data["position"].value
    if not isinstance(user_data.get("role"), str):
        user_data["role"] = user_data["role"].value
    pwd_hash: str = pwd_helper.get_password_hash(password=user_data.pop("password", None))
    user_data.update({"hashed_password": pwd_hash})
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)  # Если на стороне БД генерятся данные
    return user


async def get_total_users(db_session: AsyncSession) -> int:
    total_users: int = await db_session.scalar(select(func.count(User.id)))
    return total_users


async def get_users(db_session: AsyncSession, limit: int, offset: int) -> list[User]:
    stmt = select(User).limit(limit).offset(offset).order_by(User.created_at.desc())
    result: Result = await db_session.execute(stmt)
    users: list[User] | None = result.scalars().unique()
    if users is None:
        raise custom_exc.not_found(entity_name=User.__name__)
    return list(users)


async def get_user(db_session: AsyncSession, by_field: str, by_value: str) -> User:
    if by_field == GetUserFields.id.value:
        is_uuid: bool = is_valid_uuid(value=by_value)
        if is_uuid is False:
            raise custom_exc.invalid_input(detail="user id must by valid type UUID4")
    stmt = select(User).where(getattr(User, by_field) == by_value)

    user: User | None = await db_session.scalar(stmt)
    if user is None:
        raise custom_exc.not_found(entity_name=User.__name__)
    return user


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
        .values(**update_data.model_dump(exclude_none=True))
    )

    result: Result = await db_session.execute(stmt)
    upd_user: User = result.scalar()
    await db_session.commit()
    await db_session.refresh(upd_user)
    return upd_user


async def delete_user(db_session: AsyncSession, user_id: UUID) -> UUID:
    stmt = delete(User).returning(User).where(User.id == user_id)
    result: Result = await db_session.execute(stmt)
    user: User = result.scalar()
    if user is None:
        raise custom_exc.not_found(entity_name=User.__name__)
    if user.avatar_url != settings.default_avatar:
        try:
            # :TODO Replace to settings root path
            filepath = Path(f"src/front/static/profileimages/{user.avatar_url}")
            if filepath.is_file():
                filepath.unlink()
            else:
                print("File do not delete. Is not exists")
        except Exception as e:
            # :TODO Remove. Change to logger
            print(f"Delete file error: {e}")
    await db_session.commit()
    return user_id
