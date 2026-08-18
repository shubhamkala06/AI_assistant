from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.infrastructure.ai.checkpointer import get_checkpointer
from app.infrastructure.database import (
    dispose_database,
    initialize_database,
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting application.")

    await initialize_database()

    try:
        async with get_checkpointer() as checkpointer:
            app.state.checkpointer = checkpointer

            yield

    finally:
        await dispose_database()

        logger.info("Application shutdown complete.")
