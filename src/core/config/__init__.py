from os import path
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = "settings", "logger"

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
    debug_database: bool
    show_admin_panel: bool
    admin_panel_login: bool
    admin_auth_secret: str
    admin_username: str
    admin_password: str

    app_host: str
    app_port: int
    app_workers_count: int
    app_title: str = "API for TaskManageer"
    app_version: str = "0.1.2"
    api_v1_prefix: str = "/api/v1"
    front_prefix: str = "/front/pages"
    cookie_name_access: str = "access_token"
    default_avatar: str = "default.png"
    google_auth_scopes: list[str] = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ]
    google_auth_redirect_url: str = "http://127.0.0.1:8000/front/pages/google_callback"

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

    jwt_secret: str
    jwt_algorithm: str
    jwt_refresh_expire_min: int
    jwt_access_expire_min: int

    google_auth_client_id: str
    google_auth_client_secret: str
    session_secret: str

    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str


settings = Config()

# Настройки логирования
logger.add(
    path.join(Path(SETTINGS_DIR).parent, "logs/app.log"),
    rotation="1 MB",
    retention="7 days",
    level="INFO",
)
