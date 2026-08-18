from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.chat.model import Conversation
from app.domains.chat.repository import ConversationRepository


class ChatService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ConversationRepository(session)

    async def create_conversation(self, user_id: UUID) -> Conversation:
        return await self.repository.create(user_id)

    async def get_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> Conversation | None:
        return await self.repository.get_by_id(
            conversation_id,
            user_id,
        )
