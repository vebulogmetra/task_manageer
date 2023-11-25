from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.api_v1 import main_router as v1_router
from src.core.config import settings
from src.front import main_router as front_router
from src.utils.admin import AdminApplication
from src.utils.database import db_manager


def init_app(init_db=True) -> FastAPI:  # noqa: C901
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

    server_app = FastAPI(
        title=settings.app_title,
        version=settings.app_version,
        lifespan=lifespan,
    )

    server_app.add_middleware(
        middleware_class=SessionMiddleware, secret_key=settings.session_secret
    )

    server_app.mount("/static", StaticFiles(directory="src/front/static"), name="static")

    server_app.include_router(
        router=v1_router,
        prefix=settings.api_v1_prefix,
    )
    server_app.include_router(
        router=front_router,
        prefix=settings.front_prefix,
        tags=["Front"],
    )

    if settings.show_admin_panel:
        admin_app: AdminApplication = AdminApplication(
            server_app=server_app, db_engine=db_manager._engine
        )
        admin_app.init()
        admin_app.include_views()

    return server_app
