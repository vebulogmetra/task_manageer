from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.settings.config import settings
from src.core.utils.database import db_manager


def init_app(init_db=True) -> FastAPI:
    lifespan = None
    if init_db:
        db_manager.init(
            connection_url=settings.db_alchemy_url,
            echo=settings.debug_database,
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI):  # noqa
            yield
            if db_manager._engine is not None:
                await db_manager.close_connection()

    server = FastAPI(
        title=settings.app_title,
        version=settings.app_version,
        lifespan=lifespan,
    )

    from src.api_v1 import main_router as v1_router

    server.include_router(router=v1_router, prefix=settings.api_v1_prefix)

    return server
