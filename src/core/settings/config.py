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

    development: bool
    api_v1_prefix: str = "/api/v1"
    app_host: str
    app_port: int
    app_workers_count: int

    db_alchemy_driver: str = "postgresql+asyncpg"
    debug_database: bool
    db_host: str
    db_port: int
    db_user: str
    db_name: str
    db_password: str


settings = Config()

print(f"DEVELOPMENT: {settings.development}")
print(f"DEBUG_DATABASE: {settings.debug_database}")
