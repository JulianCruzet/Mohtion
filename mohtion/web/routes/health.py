"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "mohtion"}


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Mohtion - Autonomous Tech Debt Bounty Hunter", "version": "0.1.0"}
