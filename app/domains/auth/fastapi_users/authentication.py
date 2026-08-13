from fastapi import Depends
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
)
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)

from app.core.config import get_settings
from app.domains.auth.fastapi_users.database_adapter import get_access_token_db
from app.domains.auth.models import AccessToken

settings = get_settings()


cookie_transport = CookieTransport(
    cookie_name=settings.auth.cookie_name,
    cookie_max_age=settings.auth.access_token_lifetime_seconds,
    cookie_secure=settings.auth.cookie_secure,
    cookie_samesite=settings.auth.cookie_samesite,
)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=settings.auth.access_token_lifetime_seconds,
    )


auth_backend = AuthenticationBackend(
    name="database",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)
