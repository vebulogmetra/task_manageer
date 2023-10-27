from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api_v1 import main_router as v1_router
from src.core.settings.config import settings

# @asynccontextmanager
# async def lifespan(app: FastAPI):

#     yield


app: FastAPI = FastAPI()
app.include_router(router=v1_router, prefix=settings.api_v1_prefix)


@app.get("/")
def health_check():
    return JSONResponse("OK")
