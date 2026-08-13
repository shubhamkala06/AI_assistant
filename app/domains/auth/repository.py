from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.models import AccessToken


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def revoke_all_sessions(self, user_id: UUID) -> None:
        statement = delete(AccessToken).where(
            AccessToken.user_id == user_id,
        )

        await self.session.execute(statement)
        await self.session.commit()
