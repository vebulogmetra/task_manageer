from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.core.settings.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


sqlalchemy_url: str = f"{settings.db_alchemy_driver}://{settings.db_user}:{settings.db_password}@\
{settings.db_host}:{settings.db_port}/{settings.db_name}"

test_sqlalchemy_url: str = f"{settings.db_alchemy_driver}://{settings.test_db_user}:{settings.test_db_password}@\
{settings.test_db_host}:{settings.test_db_port}/{settings.test_db_name}"

db_helper: DatabaseHelper = DatabaseHelper(
    url=sqlalchemy_url, echo=settings.debug_database
)

test_db_helper: DatabaseHelper = DatabaseHelper(
    url=test_sqlalchemy_url, echo=settings.debug_database
)
