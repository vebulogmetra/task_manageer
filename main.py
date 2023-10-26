from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.core.models import Base
from src.core.utils.database import db_helper

# @asynccontextmanager
# async def lifespan(app: FastAPI):

#     yield


app: FastAPI = FastAPI()


@app.get("/")
def health_check():
    return JSONResponse("OK")
