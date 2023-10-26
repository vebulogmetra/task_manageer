import uvicorn

from src.core.settings.config import settings

uvicorn.run(
    "main:app",
    host=settings.app_host,
    port=settings.app_port,
    workers=settings.app_workers_count,
    reload=settings.development,
)
