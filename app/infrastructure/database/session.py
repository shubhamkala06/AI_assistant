from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.infrastructure.database.engine import primary_engine

primary_session_factory = async_sessionmaker(
    bind=primary_engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with primary_session_factory() as session:
        yield session


DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_db_session),
]
