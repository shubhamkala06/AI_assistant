from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class ConversationSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class MessageCreate(BaseModel):
    content: str


class MessageRead(BaseModel):
    role: str
    content: str


class ConversationDetail(ConversationRead):
    messages: list[MessageRead]
