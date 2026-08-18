from typing import Literal

from langchain_core.language_models import BaseChatModel

from app.infrastructure.ai.models.gemini import get_gemini_chat_model
from app.infrastructure.ai.models.openai import get_openai_chat_model

ModelProvider = Literal["google", "openai"]


def get_chat_model(provider: ModelProvider) -> BaseChatModel:
    if provider == "google":
        return get_gemini_chat_model()

    if provider == "openai":
        return get_openai_chat_model()

    raise ValueError(f"Unsupported model provider: {provider}")
