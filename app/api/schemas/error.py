from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    Standard error response returned by the API.
    """

    code: str = Field(description="Machine-readable error code.")

    message: str = Field(description="Human-readable error message.")


class ValidationErrorDetail(BaseModel):
    """
    A single validation failure.
    """

    field: str = Field(description="Field that failed validation.")

    message: str = Field(description="Validation failure message.")


class ValidationErrorResponse(ErrorResponse):
    """
    Error response for request validation failures.
    """

    errors: list[ValidationErrorDetail]
