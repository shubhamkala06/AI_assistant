from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.core.config import get_settings


@asynccontextmanager
async def get_checkpointer() -> AsyncGenerator[AsyncPostgresSaver, None]:
    settings = get_settings()

    async with AsyncPostgresSaver.from_conn_string(
        settings.database.psycopg_url,
    ) as checkpointer:
        await checkpointer.setup()

        yield checkpointer
