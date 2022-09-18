from api.api import api_router

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(api_router)
app.mount("/", StaticFiles(directory="static"), name="static")
