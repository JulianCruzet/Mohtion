"""FastAPI application factory."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from mohtion.config import get_settings
from mohtion.web.routes import health, webhooks

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)
    logger.info("Mohtion starting up...")
    yield
    logger.info("Mohtion shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Mohtion",
        description="Autonomous Tech Debt Bounty Hunter",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Register routes
    app.include_router(health.router, tags=["health"])
    app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])

    # Mount static files for landing page (must be LAST, acts as catch-all)
    static_dir = Path(__file__).parent.parent.parent / "static"
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

    return app


# Default app instance for uvicorn
app = create_app()
