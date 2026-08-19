from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.chat.model import Conversation


class ConversationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: UUID) -> Conversation:
        conversation = Conversation(user_id=user_id)

        self.session.add(conversation)

        await self.session.commit()
        await self.session.refresh(conversation)

        return conversation

    async def get_by_id(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> Conversation | None:
        result = await self.session.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
    ) -> list[Conversation]:
        result = await self.session.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )

        return list(result.scalars().all())

    async def touch(self, conversation: Conversation) -> Conversation:
        await self.session.commit()
        await self.session.refresh(conversation)

        return conversation


async def touch(self, conversation: Conversation) -> Conversation:
    conversation.updated_at = datetime.now(UTC)

    await self.session.commit()
    await self.session.refresh(conversation)

    return conversation
