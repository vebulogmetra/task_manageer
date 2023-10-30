import contextlib
from asyncio import current_task
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.core.models import Base
from src.core.settings.config import settings


class DatabaseManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    def init(self, connection_url: str, echo: Optional[bool] = False):
        self._engine = create_async_engine(url=connection_url, echo=echo)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def close_connection(self):
        if self._engine is None:
            raise Exception("Database session is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._session_factory = None

    @contextlib.asynccontextmanager
    async def get_connection(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("Database session is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def scoped_session_dependency(self):
        if self._session_factory is None:
            raise Exception("Database session is not initialized")
        scoped_factory = async_scoped_session(
            session_factory=self._session_factory,
            scopefunc=current_task,
        )
        try:
            async with scoped_factory() as scoped:
                yield scoped
        finally:
            await scoped_factory.remove()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


db_manager = DatabaseManager()


async def get_db() -> AsyncIterator[AsyncSession]:
    async with db_manager.scoped_session_dependency() as session:
        yield session
