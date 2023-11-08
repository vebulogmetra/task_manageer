import asyncio
from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.ext.asyncio import AsyncConnection

from src import init_app
from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.auth.service import create_tokens
from src.api_v1.base.models import Base
from src.core.config import settings
from src.utils.database import db_manager, get_db
from tests.integration.resources import test_user


async def db_create_all(connection: AsyncConnection):
    await connection.run_sync(Base.metadata.create_all)


async def db_drop_all(connection: AsyncConnection):
    await connection.run_sync(Base.metadata.drop_all)


# Init app without db
@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


# Create test db
test_db = factories.postgresql_proc(port=None, dbname=settings.test_db_name)


# Create event loop for test session (default for function)
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Create test db connection
@pytest.fixture(scope="session", autouse=True)
async def connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        user=pg_user,
        host=pg_host,
        port=pg_port,
        dbname=pg_db,
        version=test_db.version,
        password=pg_password,
    ):
        connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        db_manager.init(connection_url=connection_str, echo=False)
        yield
        await db_manager.close_connection()


@pytest.fixture(scope="module", autouse=True)
async def create_tables(connection_test):
    async with db_manager.get_connection() as connection:
        await db_drop_all(connection)
        await db_create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with db_manager.scoped_session_dependency() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override


def get_user_token(user_id: str, user_email: str):
    access_token = create_tokens(
        user_data=TokenUserData(id=user_id, email=user_email)
    ).access_token
    return access_token


@pytest.fixture
def access_token(client):
    login_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    login_data = {"username": test_user.email, "password": test_user.password}

    response = client.post("/api/v1/auth/login", headers=login_headers, data=login_data)
    access_token = response.json()["access_token"]
    return access_token
