from langchain_openai import ChatOpenAI

from app.core.config import get_settings


def get_openai_chat_model() -> ChatOpenAI:
    settings = get_settings()

    if not settings.ai.openai_api_key:
        raise RuntimeError("OpenAI API key is not configured.")

    if not settings.ai.openai_chat_model:
        raise RuntimeError("OpenAI chat model is not configured.")

    return ChatOpenAI(
        model=settings.ai.openai_chat_model,
        api_key=settings.ai.openai_api_key,
    )
