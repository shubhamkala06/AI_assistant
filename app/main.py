from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions.exception_handlers import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.observability.logging import configure_logging
from app.core.observability.middleware import (
    AccessLogMiddleware,
)

settings = get_settings()

configure_logging(settings)

app = FastAPI(
    title=settings.app.app_name,
    debug=settings.app.debug,
    lifespan=lifespan,
)

# Middleware executes in reverse registration order.
# CorrelationIdMiddleware must execute before AccessLogMiddleware
# so that the request ID is available in all application logs.
app.add_middleware(AccessLogMiddleware)
app.add_middleware(CorrelationIdMiddleware)

register_exception_handlers(app)

app.include_router(api_router)
