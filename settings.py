from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=('.env', '.env.stag', '.env.prod'),
                                      env_file_encoding="utf-8",
                                      extra='ignore')
    development: bool
    app_host: str
    app_port: int
    app_workers_count: int


app_settings = Config()
