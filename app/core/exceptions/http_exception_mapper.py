from http import HTTPStatus

from app.core.exceptions.exceptions import (
    ApplicationException,
    ConfigurationError,
    DependencyUnavailable,
    InternalServerError,
    ValidationError,
)

HTTP_STATUS_MAPPING: dict[type[ApplicationException], HTTPStatus] = {
    ValidationError: HTTPStatus.BAD_REQUEST,
    DependencyUnavailable: HTTPStatus.SERVICE_UNAVAILABLE,
    ConfigurationError: HTTPStatus.INTERNAL_SERVER_ERROR,
    InternalServerError: HTTPStatus.INTERNAL_SERVER_ERROR,
}


def register_exception_status(
    exception_cls: type[ApplicationException],
    http_status: HTTPStatus,
) -> None:
    if exception_cls in HTTP_STATUS_MAPPING:
        raise RuntimeError(
            f"HTTP status mapping already registered for '{exception_cls.__name__}'."
        )

    HTTP_STATUS_MAPPING[exception_cls] = http_status


def get_http_status(exc: ApplicationException) -> HTTPStatus:
    try:
        return HTTP_STATUS_MAPPING[type(exc)]
    except KeyError as e:
        raise RuntimeError(
            f"No HTTP status mapping exists for '{type(exc).__name__}'."
        ) from e
