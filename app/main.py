from api.api import api_router

from fastapi import FastAPI

app = FastAPI()
app.include_router(api_router)
