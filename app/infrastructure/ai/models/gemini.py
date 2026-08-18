from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings


def get_gemini_chat_model() -> ChatGoogleGenerativeAI:
    settings = get_settings()

    if not settings.ai.google_api_key:
        raise RuntimeError("Google API key is not configured.")

    if not settings.ai.gemini_chat_model:
        raise RuntimeError("Gemini chat model is not configured.")

    return ChatGoogleGenerativeAI(
        model=settings.ai.gemini_chat_model,
        google_api_key=settings.ai.google_api_key,
    )
