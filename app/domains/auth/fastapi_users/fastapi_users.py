import uuid

from fastapi_users import FastAPIUsers
from httpx_oauth.clients.google import GoogleOAuth2

from app.core.config import get_settings
from app.domains.auth.fastapi_users.authentication import auth_backend
from app.domains.auth.fastapi_users.manager import get_user_manager
from app.domains.users.models import User

settings = get_settings()


google_oauth_client = GoogleOAuth2(
    client_id=settings.auth.google_client_id,
    client_secret=settings.auth.google_client_secret,
)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
