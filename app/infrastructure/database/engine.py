import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    create_async_engine,
)

from app.core.config import get_settings

logger = structlog.get_logger(__name__)

settings = get_settings()

primary_engine: AsyncEngine = create_async_engine(
    settings.database.url,
    echo=settings.database.echo,
    pool_pre_ping=True,
)


async def initialize_database() -> None:
    """
    Verify database connectivity during application startup.

    Raises:
        DependencyUnavailable:
            If the database cannot be reached.
    """

    logger.info("Initializing database connection.")

    try:
        async with primary_engine.connect() as connection:
            await _verify_connection(connection)

    except Exception:
        logger.exception("Failed to initialize database.")

        # TODO:
        # Raise DatabaseUnavailable from exc
        # once the database domain exceptions are introduced.
        raise

    logger.info("Database connection established.")


async def dispose_database() -> None:
    """
    Dispose the SQLAlchemy engine.
    """

    logger.info("Disposing database engine.")

    await primary_engine.dispose()

    logger.info("Database engine disposed.")


# async def _verify_connection(
#     connection: AsyncConnection,
# ) -> None:
#     """
#     Execute a lightweight query to verify connectivity.
#     """

#     await connection.execute(text("SELECT 1"))


async def _verify_connection(
    connection: AsyncConnection,
) -> None:
    """
    Verify connectivity and print all database tables.
    """

    result = await connection.execute(
        text(
            """
            SELECT tablename
            FROM pg_catalog.pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename
            """
        )
    )

    tables = result.scalars().all()

    print("Database tables:")
    for table in tables:
        print(f"  - {table}")
