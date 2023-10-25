from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings


db_url: str = settings.get_sqlalchemy_db_url()

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

db_helper: DatabaseHelper = DatabaseHelper(url=db_url, echo=False)
