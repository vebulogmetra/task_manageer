from os import path
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

SETTINGS_DIR: str = Path(__file__).parent


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            path.join(SETTINGS_DIR, ".env"),
            path.join(SETTINGS_DIR, ".env.stag"),
            path.join(SETTINGS_DIR, ".env.prod"),
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )
    api_v1_prefix: str = "/api/v1"
    development: bool
    app_host: str
    app_port: int
    app_workers_count: int
    db_host: str
    db_port: int
    db_user: str
    db_name: str
    db_password: str

    def get_sqlalchemy_db_url(self) -> str:
        url: str = f"postgresql+asyncpg://{self.db_user}:{self.db_password}@\
{self.db_host}:{self.db_port}/{self.db_name}"
        return url


settings = Config()
