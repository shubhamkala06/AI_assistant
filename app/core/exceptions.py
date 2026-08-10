from __future__ import annotations

from abc import ABC
from typing import Any, ClassVar

from app.core.error_codes import CoreErrorCode


class ApplicationException(Exception, ABC):
    """
    Base class for all application exceptions.

    Application exceptions expose:
        - a machine-readable error code
        - a user-facing message
        - an optional internal message
        - optional metadata for logging

    They intentionally contain no HTTP knowledge.
    """

    ERROR_CODE: ClassVar[str | CoreErrorCode]
    MESSAGE: ClassVar[str]

    def __init__(
        self,
        *,
        message: str | None = None,
        internal_message: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.message = self.MESSAGE if message is None else message
        self.internal_message = internal_message
        self.metadata = metadata or {}

        super().__init__(internal_message or self.message)

    @property
    def error_code(self) -> str:
        return str(self.ERROR_CODE)


class BusinessError(ApplicationException, ABC):
    """
    Base class for expected business failures.

    Business errors represent situations where the system
    behaved correctly but the requested operation could
    not be completed because of business rules.
    """


class SystemError(ApplicationException, ABC):
    """
    Base class for unexpected infrastructure failures.

    These generally indicate problems with dependencies
    or application configuration.
    """


class ValidationError(BusinessError):
    ERROR_CODE = CoreErrorCode.VALIDATION_ERROR
    MESSAGE = "Request validation failed."


class DependencyUnavailable(SystemError):
    ERROR_CODE = CoreErrorCode.DEPENDENCY_UNAVAILABLE
    MESSAGE = "A required dependency is currently unavailable."


class ConfigurationError(SystemError):
    ERROR_CODE = CoreErrorCode.CONFIGURATION_ERROR
    MESSAGE = "The application is incorrectly configured."


class InternalServerError(SystemError):
    ERROR_CODE = CoreErrorCode.INTERNAL_SERVER_ERROR
    MESSAGE = "An unexpected error occurred."
