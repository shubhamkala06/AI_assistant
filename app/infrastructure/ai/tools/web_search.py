from langchain_tavily import TavilySearch

from app.core.config import get_settings


def get_web_search_tool() -> TavilySearch:
    settings = get_settings()

    if not settings.ai.tavily_api_key:
        raise RuntimeError("Tavily API key is not configured.")

    return TavilySearch(
        tavily_api_key=settings.ai.tavily_api_key,
        max_results=5,
        search_depth="basic",
        topic="general",
        include_answer="basic",
        include_raw_content=False,
    )
