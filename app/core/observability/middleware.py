import time

import structlog
from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)
from starlette.responses import Response

logger = structlog.get_logger(__name__)


class AccessLogMiddleware(BaseHTTPMiddleware):
    """
    Logs one entry at the beginning and one at the end of every request.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        start = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )

        return response
