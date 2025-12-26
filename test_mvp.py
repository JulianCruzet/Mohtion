#!/usr/bin/env python3
"""
Simple MVP test script - runs the Mohtion agent loop on a test repository.

This script bypasses the job queue and runs the orchestrator directly,
which is useful for testing without Docker/Redis.
"""
import asyncio
import logging

from mohtion.agent.orchestrator import Orchestrator
from mohtion.integrations.github_api import GitHubAPI
from mohtion.integrations.github_app import GitHubApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_scan_repository(owner: str, repo: str, installation_id: int):
    """
    Test the full Mohtion agent loop on a repository.

    Args:
        owner: GitHub repository owner
        repo: GitHub repository name
        installation_id: GitHub App installation ID
    """
    logger.info("=" * 60)
    logger.info(f"Starting Mohtion MVP test on {owner}/{repo}")
    logger.info("=" * 60)

    # Initialize GitHub App and API client
    github_app = GitHubApp()
    github_api = GitHubAPI(github_app, installation_id)

    # Run the orchestrator
    orchestrator = Orchestrator(github_api, owner, repo)

    try:
        result = await orchestrator.run()

        if result:
            logger.info("=" * 60)
            logger.info("SUCCESS! Bounty result:")
            logger.info(f"  Status: {result.status.value}")
            logger.info(f"  Branch: {result.branch_name}")
            logger.info(f"  Target: {result.target.location}")
            logger.info(f"  PR URL: {result.pr_url}")
            logger.info(f"  Tests passed: {result.test_passed}")
            logger.info(f"  Retry count: {result.retry_count}")
            logger.info("=" * 60)
        else:
            logger.info("=" * 60)
            logger.info("No tech debt targets found in repository")
            logger.info("=" * 60)

        return result

    except Exception as e:
        logger.exception("Orchestrator failed")
        raise


async def main():
    """Main entry point for MVP testing."""

    # CONFIGURED FOR YOUR REPOSITORY:
    OWNER = "JulianCruzet"
    REPO = "Newtons-Cradle"
    INSTALLATION_ID = 101273572

    # Run the test
    await test_scan_repository(OWNER, REPO, INSTALLATION_ID)


if __name__ == "__main__":
    asyncio.run(main())
