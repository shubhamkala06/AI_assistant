from fastapi import APIRouter, Depends

from app.domains.auth.dependencies import current_user
from app.domains.users.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/profile", response_model=None)
async def get_profile(
    user: User = Depends(current_user),
) -> User:
    return user
