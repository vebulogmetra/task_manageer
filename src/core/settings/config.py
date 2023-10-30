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
    app_title: str = "API for TaskManageer"
    app_version: str = "0.1.1"
    api_v1_prefix: str = "/api/v1"
    app_host: str
    app_port: int
    app_workers_count: int

    debug_database: bool

    db_host: str
    db_port: int
    db_user: str
    db_name: str
    db_password: str
    db_alchemy_url: str

    test_db_host: str
    test_db_port: int
    test_db_user: str
    test_db_name: str
    test_db_password: str
    test_db_alchemy_url: str


settings = Config()

print(f"DEVELOPMENT: {settings.development}")
print(f"DEBUG_DATABASE: {settings.debug_database}")
