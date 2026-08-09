from contextlib import asynccontextmanager

import structlog

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app):
    logger.info("application starting")

    yield

    logger.info("application stopping")
