import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.core.config import get_settings
from app.domains.auth.fastapi_users.database_adapter import get_user_db
from app.domains.users.models import User

settings = get_settings()


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.auth.reset_password_token_secret
    verification_token_secret = settings.auth.verification_token_secret


async def get_user_manager(
    user_db=Depends(get_user_db),
):
    yield UserManager(user_db)
