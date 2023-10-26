from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.core.models import Base
from src.core.utils.database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
    yield


app: FastAPI = FastAPI(lifespan=lifespan)


@app.get("/")
def health_check():
    return JSONResponse("OK")
