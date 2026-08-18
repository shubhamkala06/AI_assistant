from deepagents import create_deep_agent
from langgraph.graph.state import CompiledStateGraph

from app.infrastructure.ai.models.factory import get_chat_model
from app.infrastructure.ai.prompts.normal_agent import NORMAL_CHAT_SYSTEM_PROMPT
from app.infrastructure.ai.tools.web_search import get_web_search_tool


def build_normal_agent(checkpointer) -> CompiledStateGraph:
    return create_deep_agent(
        model=get_chat_model(),
        tools=[get_web_search_tool()],
        system_prompt=NORMAL_CHAT_SYSTEM_PROMPT,
        checkpointer=checkpointer,
        name="normal_chat_agent",
    )
