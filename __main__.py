import uvicorn
from settings import (
    DEVELOPMENT,
    APP_HOST,
    APP_PORT,
    APP_WORKERS_COUNT
)


uvicorn.run("main:app",
            host=APP_HOST,
            port=APP_PORT,
            workers=APP_WORKERS_COUNT,
            reload=DEVELOPMENT)
