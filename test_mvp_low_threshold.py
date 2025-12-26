#!/usr/bin/env python3
"""MVP test script with lowered complexity threshold."""
import asyncio
import logging
import tempfile
from pathlib import Path

from mohtion.agent.scanner import Scanner
from mohtion.integrations.github_api import GitHubAPI
from mohtion.integrations.github_app import GitHubApp
from mohtion.models.repo_config import RepoConfig, Thresholds

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_scan_with_low_threshold(owner: str, repo: str, installation_id: int):
    """Test scanning with a lower complexity threshold."""
    logger.info("=" * 60)
    logger.info(f"Scanning {owner}/{repo} with LOW threshold (5)")
    logger.info("=" * 60)

    # Initialize GitHub App and API client
    github_app = GitHubApp()
    github_api = GitHubAPI(github_app, installation_id)

    try:
        # Clone the repository
        logger.info(f"Cloning {owner}/{repo}...")
        repo_path = await github_api.clone_repo(owner, repo)
        logger.info(f"Cloned to {repo_path}")

        # Create config with LOW threshold
        config = RepoConfig(
            thresholds=Thresholds(
                cyclomatic_complexity=5,  # Much lower threshold!
                function_length=50,
                nesting_depth=4
            )
        )

        # Run scanner
        scanner = Scanner(repo_path, config)
        targets = await scanner.scan()

        if targets:
            logger.info("=" * 60)
            logger.info(f"Found {len(targets)} tech debt target(s):")
            logger.info("=" * 60)
            for i, target in enumerate(targets, 1):
                logger.info(f"\n{i}. {target}")
                logger.info(f"   Severity: {target.severity:.2f}")
                logger.info(f"   Metric: {target.metric_value}")
                logger.info(f"   Description: {target.description}")
        else:
            logger.info("=" * 60)
            logger.info("Still no targets found - code is very clean!")
            logger.info("=" * 60)

        # Note: Not cleaning up the temp directory to avoid Windows permission errors
        logger.info(f"\nTemp directory kept at: {repo_path}")
        logger.info("(You can delete it manually later)")

    except Exception as e:
        logger.exception("Scan failed")
        raise


async def main():
    """Main entry point for MVP testing."""
    OWNER = "JulianCruzet"
    REPO = "Newtons-Cradle"
    INSTALLATION_ID = 101273572

    await test_scan_with_low_threshold(OWNER, REPO, INSTALLATION_ID)


if __name__ == "__main__":
    asyncio.run(main())
