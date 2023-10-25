from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=('.env', '.env.stag', '.env.prod'),
                                      env_file_encoding="utf-8",
                                      extra='ignore')
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


