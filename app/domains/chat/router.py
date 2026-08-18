from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.domains.auth.dependencies import current_user
from app.domains.chat.schemas import ConversationRead
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
    "/{conversation_id}",
    response_model=ConversationRead,
)
async def get_conversation(
    conversation_id: UUID,
    session: DatabaseSession,
    user: User = Depends(current_user),
) -> ConversationRead:
    service = ChatService(session)

    conversation = await service.get_conversation(
        conversation_id,
        user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    return ConversationRead.model_validate(conversation)
