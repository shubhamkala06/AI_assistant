from fastapi import APIRouter, Depends, Response, status

from app.core.config import get_settings
from app.domains.auth.dependencies import current_user
from app.domains.auth.fastapi_users.authentication import auth_backend
from app.domains.auth.fastapi_users.fastapi_users import (
    fastapi_users,
    google_oauth_client,
)
from app.domains.auth.schemas import UserCreate, UserRead
from app.domains.auth.service import AuthService
from app.domains.users.models import User
from app.infrastructure.database.session import DatabaseSession

settings = get_settings()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

router.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)

# router.include_router(
#     fastapi_users.get_reset_password_router(),
# )

router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        settings.auth.oauth_state_secret,
    ),
    prefix="/google",
)


@router.post(
    "/logout-all",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_everywhere(
    session: DatabaseSession,
    user: User = Depends(current_user),
) -> Response:
    service = AuthService(session)

    await service.logout_everywhere(user.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
