from http import HTTPStatus

# from app.domains.users.exceptions import (
#     UserAlreadyExists,
#     UserInactive,
#     UserNotFound,
# )
from app.core.exceptions import (
    ApplicationException,
    ConfigurationError,
    DependencyUnavailable,
    InternalServerError,
    ValidationError,
)

HTTP_STATUS_MAPPING: dict[type[ApplicationException], HTTPStatus] = {
    #
    # Core
    #
    ValidationError: HTTPStatus.BAD_REQUEST,
    DependencyUnavailable: HTTPStatus.SERVICE_UNAVAILABLE,
    ConfigurationError: HTTPStatus.INTERNAL_SERVER_ERROR,
    InternalServerError: HTTPStatus.INTERNAL_SERVER_ERROR,
    #
    # Users
    #
    # UserNotFound: HTTPStatus.NOT_FOUND,
    # UserAlreadyExists: HTTPStatus.CONFLICT,
    # UserInactive: HTTPStatus.FORBIDDEN,
}


def get_http_status(exc: ApplicationException) -> HTTPStatus:
    """
    Returns the HTTP status code corresponding to an application exception.
    """

    try:
        return HTTP_STATUS_MAPPING[type(exc)]
    except KeyError as e:
        raise RuntimeError(
            f"No HTTP status mapping exists for '{type(exc).__name__}'."
        ) from e
