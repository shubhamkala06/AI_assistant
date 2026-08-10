import structlog
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.schemas.error import (
    ErrorResponse,
    ValidationErrorDetail,
    ValidationErrorResponse,
)
from app.core.exceptions.error_codes import CoreErrorCode
from app.core.exceptions.exceptions import (
    ApplicationException,
    InternalServerError,
    SystemError,
    ValidationError,
)
from app.core.exceptions.http_exception_mapper import get_http_status

logger = structlog.get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationException)
    async def application_exception_handler(
        request: Request,
        exc: ApplicationException,
    ) -> JSONResponse:
        if isinstance(exc, SystemError):
            logger.error(
                "application_exception",
                error_code=exc.error_code,
                message=exc.message,
                internal_message=exc.internal_message,
                metadata=exc.metadata,
                exc_info=True,
            )

        response = ErrorResponse(
            code=exc.error_code,
            message=exc.message,
        )

        return JSONResponse(
            status_code=get_http_status(exc),
            content=response.model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        validation_errors: list[ValidationErrorDetail] = []

        for error in exc.errors():
            field = ".".join(str(part) for part in error["loc"] if part != "body")

            validation_errors.append(
                ValidationErrorDetail(
                    field=field,
                    message=error["msg"],
                )
            )

        logger.info(
            "request_validation_failed",
            validation_errors=exc.errors(),
        )

        response = ValidationErrorResponse(
            code=CoreErrorCode.VALIDATION_ERROR,
            message=ValidationError.MESSAGE,
            errors=validation_errors,
        )

        return JSONResponse(
            status_code=get_http_status(ValidationError()),
            content=response.model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception("unhandled_exception")

        internal_error = InternalServerError()

        response = ErrorResponse(
            code=internal_error.error_code,
            message=internal_error.message,
        )

        return JSONResponse(
            status_code=get_http_status(internal_error),
            content=response.model_dump(),
        )
