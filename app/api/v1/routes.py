from fastapi import APIRouter
from .endpoints.auth import router as auth_router
from .endpoints.user import router as users_router

routers = APIRouter(
    prefix="/api/v1"
)
routers.include_router(auth_router)
routers.include_router(users_router)