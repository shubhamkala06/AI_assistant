from fastapi import FastAPI

from app.api.router import api_router
from app.core.lifespan import lifespan

app = FastAPI(
    title="AI Assistant",
    lifespan=lifespan,
)

app.include_router(api_router)
