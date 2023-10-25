from dotenv import load_dotenv
from os import environ



try:
    load_dotenv()
except Exception as err:
    print("Envfile load error: \n", err)


DEVELOPMENT: bool = bool(environ.get("DEVELOPMENT"))
APP_HOST: str = environ.get("APP_HOST")
APP_PORT: int = int(environ.get("APP_PORT"))
APP_WORKERS_COUNT: int = int(environ.get("APP_WORKERS_COUNT"))
