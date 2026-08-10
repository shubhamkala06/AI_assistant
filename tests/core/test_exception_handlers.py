from unittest.mock import Mock

import pytest
from fastapi import FastAPI, Request

from app.core.exception_handlers import register_exception_handlers
from app.core.exceptions import ApplicationException, InternalServerError


@pytest.mark.asyncio
async def test_system_error_logs_with_exc_info(monkeypatch):
    app = FastAPI()
    register_exception_handlers(app)

    logger_error = Mock()

    monkeypatch.setattr(
        "app.core.exception_handlers.logger.error",
        logger_error,
    )

    handler = app.exception_handlers[ApplicationException]

    exc = InternalServerError(
        public_message="Something went wrong.",
        internal_message="Database connection failed.",
        metadata={"service": "database"},
    )

    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "headers": [],
        }
    )

    await handler(request, exc)

    logger_error.assert_called_once_with(
        "application_exception",
        error_code=exc.error_code,
        public_message=exc.public_message,
        internal_message=exc.internal_message,
        metadata=exc.metadata,
        exc_info=True,
    )
