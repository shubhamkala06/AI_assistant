from collections.abc import AsyncGenerator
from uuid import UUID

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
)

from app.domains.auth.models import AccessToken
from app.domains.users.models import User
from app.infrastructure.database.session import DatabaseSession


async def get_user_db(
    session: DatabaseSession,
) -> AsyncGenerator[SQLAlchemyUserDatabase[User, UUID], None]:
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_db(
    session: DatabaseSession,
) -> AsyncGenerator[SQLAlchemyAccessTokenDatabase[AccessToken], None]:
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
