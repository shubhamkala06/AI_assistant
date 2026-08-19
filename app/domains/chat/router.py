from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.domains.auth.dependencies import current_user
from app.domains.chat.schemas import (
    ConversationDetail,
    ConversationRead,
    ConversationSummary,
    MessageCreate,
    MessageRead,
)
from app.domains.chat.service import ChatService
from app.domains.users.models import User
from app.infrastructure.database.session import DatabaseSession

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=ConversationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_conversation(
    session: DatabaseSession,
    user: User = Depends(current_user),
) -> ConversationRead:
    service = ChatService(session)

    conversation = await service.create_conversation(user.id)

    return ConversationRead.model_validate(conversation)


@router.get(
    "",
    response_model=list[ConversationSummary],
)
async def list_conversations(
    session: DatabaseSession,
    user: User = Depends(current_user),
) -> list[ConversationSummary]:
    service = ChatService(session)

    conversations = await service.list_conversations(user.id)

    return [
        ConversationSummary.model_validate(conversation)
        for conversation in conversations
    ]


@router.get(
    "/{conversation_id}",
    response_model=ConversationDetail,
)
async def get_conversation(
    conversation_id: UUID,
    session: DatabaseSession,
    user: User = Depends(current_user),
) -> ConversationDetail:
    service = ChatService(session)

    conversation = await service.get_conversation_detail(
        conversation_id,
        user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    return conversation


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageRead,
)
async def send_message(
    conversation_id: UUID,
    message: MessageCreate,
    session: DatabaseSession,
    user: User = Depends(current_user),
) -> MessageRead:
    service = ChatService(session)

    response = await service.send_message(
        conversation_id,
        user.id,
        message.content,
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    return MessageRead(
        role="assistant",
        content=response,
    )
