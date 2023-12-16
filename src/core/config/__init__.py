from os import path, getenv
from pathlib import Path

from fastapi.templating import Jinja2Templates
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
    app_version: str = "0.1.4"
    api_v1_prefix: str = "/api/v1"
    front_prefix: str = "/front/pages"
    cookie_name_access: str = "access_token"
    default_avatar: str = "default.png"
    html_staticfiles_path: str = "src/front/static"
    html_templates_path: str = "src/front/templates"

    db_alchemy_url: str
    db_alchemy_url_docker: str

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

    google_auth_grant_type: str = "authorization_code"
    google_auth_client_id: str
    google_auth_client_secret: str
    google_auth_conf_url: str
    google_auth_scopes: list[str] = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ]
    google_auth_redirect_url: str = "http://127.0.0.1:8000/api/v1/auth/google/callback"
    google_auth_base_url: str = "https://accounts.google.com/o/oauth2/auth"
    google_auth_get_id_token_url: str = "https://oauth2.googleapis.com/token"

    session_secret: str

    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str

    elasticsearch_url: str
    elasticsearch_url_docker: str


settings = Config()

html_templates = Jinja2Templates(directory=settings.html_templates_path)

# Настройки логирования
logger.add(
    path.join(Path(SETTINGS_DIR).parent, "logs/app.log"),
    rotation="1 MB",
    retention="7 days",
    level="INFO",
)

# Изменение подключения к сервисам при запуске в docker

if getenv("DOKERIZE") == "True":
    settings.db_alchemy_url = settings.db_alchemy_url_docker
    settings.elasticsearch_url = settings.elasticsearch_url_docker
