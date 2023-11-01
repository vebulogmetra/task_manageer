import uvicorn

from src.core.config import settings

print(f"DEVELOPMENT: {settings.development}")
print(f"DEBUG_DATABASE: {settings.debug_database}")

uvicorn.run(
    "main:server",
    host=settings.app_host,
    port=settings.app_port,
    workers=settings.app_workers_count,
    reload=settings.development,
)
