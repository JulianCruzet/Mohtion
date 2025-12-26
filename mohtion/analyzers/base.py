"""Base analyzer interface."""

from abc import ABC, abstractmethod
from pathlib import Path

from mohtion.models.repo_config import RepoConfig
from mohtion.models.target import TechDebtTarget


class Analyzer(ABC):
    """Abstract base class for code analyzers."""

    def __init__(self, config: RepoConfig) -> None:
        self.config = config

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the analyzer name."""
        ...

    @abstractmethod
    async def analyze_file(self, file_path: Path, content: str) -> list[TechDebtTarget]:
        """
        Analyze a single file for tech debt.

        Args:
            file_path: Path to the file (relative to repo root)
            content: File content as string

        Returns:
            List of tech debt targets found in the file
        """
        ...

    def should_analyze(self, file_path: Path) -> bool:
        """Check if this file should be analyzed."""
        # Check if file matches any ignore patterns
        import fnmatch

        path_str = str(file_path)
        for pattern in self.config.ignore_paths:
            if fnmatch.fnmatch(path_str, pattern):
                return False
        return True
