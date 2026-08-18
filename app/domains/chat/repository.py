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
