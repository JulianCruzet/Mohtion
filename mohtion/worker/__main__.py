"""Worker entry point for `python -m mohtion.worker`."""

import asyncio
import logging

from mohtion.worker.main import run_worker

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    asyncio.run(run_worker())
