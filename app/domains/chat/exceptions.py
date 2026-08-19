from http import HTTPStatus

from app.core.exceptions.exceptions import BusinessError
from app.core.exceptions.http_exception_mapper import register_exception_status


class ConversationNotFound(BusinessError):
    ERROR_CODE = "CONVERSATION_NOT_FOUND"
    MESSAGE = "Conversation not found."


register_exception_status(
    ConversationNotFound,
    HTTPStatus.NOT_FOUND,
)
