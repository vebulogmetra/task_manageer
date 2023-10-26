import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.user import User
from src.core.utils.database import db_helper


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print(f"User: {user}")
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    print(f"User: {user}")
    # 2 способ, scalar также возвращает None если записи нет
    # user: User | None = session.scalar(stmt)
    return user


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="PetrTest")
        # await create_user(session=session, username="JohnTest")
        await get_user_by_username(session=session, username="string")  # Not exists
        await get_user_by_username(session=session, username="JohnTest")


if __name__ == "__main__":
    asyncio.run(main())
