from fastapi import APIRouter

from api.endpoints import get_data

api_router = APIRouter()
api_router.include_router(get_data.router)
