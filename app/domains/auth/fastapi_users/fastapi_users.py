import uuid

from fastapi_users import FastAPIUsers

from app.domains.auth.fastapi_users.authentication import auth_backend
from app.domains.auth.fastapi_users.manager import get_user_manager
from app.domains.users.models import User

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
