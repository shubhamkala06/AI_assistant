from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.domains.auth.router import router as auth_router
from app.domains.chat.router import router as chat_router
from app.domains.users.router import router as user_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(chat_router)
