from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.chat.model import Conversation
from app.domains.chat.repository import ConversationRepository
from app.domains.chat.schemas import ConversationDetail, MessageRead
from app.domains.chat.utils import _message_to_read
from app.infrastructure.ai.agents.normal_agent import build_normal_agent
from app.infrastructure.ai.checkpointer import get_checkpointer


class ChatService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ConversationRepository(session)

    async def create_conversation(self, user_id: UUID) -> Conversation:
        return await self.repository.create(user_id)

    async def list_conversations(
        self,
        user_id: UUID,
    ) -> list[Conversation]:
        return await self.repository.list_by_user(user_id)

    async def get_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> Conversation | None:
        return await self.repository.get_by_id(
            conversation_id,
            user_id,
        )

    async def send_message(
        self,
        conversation_id: UUID,
        user_id: UUID,
        content: str,
    ) -> str | None:
        conversation = await self.repository.get_by_id(
            conversation_id,
            user_id,
        )

        if conversation is None:
            return None

        config = {
            "configurable": {
                "thread_id": str(conversation.id),
            }
        }

        async with get_checkpointer() as checkpointer:
            agent = build_normal_agent(checkpointer)

            result = await agent.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": content,
                        }
                    ]
                },
                config,
            )

        await self.repository.touch(conversation)

        return result["messages"][-1].text

    async def get_messages(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ):
        conversation = await self.repository.get_by_id(
            conversation_id,
            user_id,
        )

        if conversation is None:
            return None

        config = {
            "configurable": {
                "thread_id": str(conversation.id),
            }
        }

        async with get_checkpointer() as checkpointer:
            agent = build_normal_agent(checkpointer)

            state = await agent.aget_state(config)

        return conversation, state.values.get("messages", [])

    async def get_conversation_detail(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> ConversationDetail | None:
        result = await self.get_messages(
            conversation_id,
            user_id,
        )

        if result is None:
            return None

        conversation, raw_messages = result

        messages: list[MessageRead] = []

        for message in raw_messages:
            message_read = _message_to_read(message)

            if message_read is not None:
                messages.append(message_read)

        return ConversationDetail(
            id=conversation.id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=messages,
        )
