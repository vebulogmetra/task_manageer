from fastapi import FastAPI
from fastapi.responses import JSONResponse

app: FastAPI = FastAPI()

@app.get("/")
def health_check():
    return JSONResponse("OK")
