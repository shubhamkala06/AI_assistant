from enum import StrEnum


class CoreErrorCode(StrEnum):
    """Core framework error codes.

    Error codes that are owned by the application core.

    These represent framework-level failures rather than
    domain-specific business errors.
    """

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

    VALIDATION_ERROR = "VALIDATION_ERROR"

    DEPENDENCY_UNAVAILABLE = "DEPENDENCY_UNAVAILABLE"

    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
