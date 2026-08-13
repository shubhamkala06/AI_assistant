from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.repository import AuthRepository


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AuthRepository(session)

    async def logout_everywhere(self, user_id: UUID) -> None:
        await self.repository.revoke_all_sessions(user_id)
