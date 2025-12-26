"""ARQ worker configuration and runner."""

import logging

from arq import create_pool
from arq.connections import RedisSettings

from mohtion.config import get_settings
from mohtion.worker.tasks import scan_repository

logger = logging.getLogger(__name__)


def get_redis_settings() -> RedisSettings:
    """Parse Redis URL into ARQ settings."""
    settings = get_settings()
    # Parse redis://host:port format
    url = settings.redis_url.replace("redis://", "")
    if ":" in url:
        host, port = url.split(":")
        return RedisSettings(host=host, port=int(port))
    return RedisSettings(host=url)


class WorkerSettings:
    """ARQ worker settings."""

    functions = [scan_repository]
    redis_settings = get_redis_settings()

    # Worker configuration
    max_jobs = 5
    job_timeout = 600  # 10 minutes per job
    keep_result = 3600  # Keep results for 1 hour

    @staticmethod
    async def on_startup(ctx: dict) -> None:
        """Called when worker starts."""
        logger.info("Mohtion worker starting...")

    @staticmethod
    async def on_shutdown(ctx: dict) -> None:
        """Called when worker shuts down."""
        logger.info("Mohtion worker shutting down...")


async def run_worker() -> None:
    """Run the ARQ worker."""
    from arq import run_worker as arq_run_worker

    await arq_run_worker(WorkerSettings)  # type: ignore[arg-type]


async def enqueue_scan(
    owner: str, repo: str, installation_id: int, branch: str = "main"
) -> str:
    """Enqueue a repository scan job."""
    redis = await create_pool(get_redis_settings())
    job = await redis.enqueue_job(
        "scan_repository",
        owner=owner,
        repo=repo,
        installation_id=installation_id,
        branch=branch,
    )
    await redis.close()
    return job.job_id if job else ""
