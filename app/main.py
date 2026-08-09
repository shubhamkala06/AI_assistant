from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.lifespan import lifespan
from app.core.logging import configure_logging

settings = get_settings()

configure_logging(settings)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(api_router)
