"""Repository configuration model - parsed from .mohtion.yaml."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Thresholds:
    """Configurable thresholds for debt detection."""

    cyclomatic_complexity: int = 10
    function_length: int = 50
    nesting_depth: int = 4


@dataclass
class RepoConfig:
    """Configuration for Mohtion on a specific repository."""

    # Scanning
    scan_interval: str = "24h"
    max_prs_per_day: int = 3

    # Test execution
    test_command: str | None = None  # Auto-detect if not specified

    # Enabled analyzers
    analyzers: list[str] = field(
        default_factory=lambda: ["complexity", "type_hints", "duplicates"]
    )

    # Thresholds
    thresholds: Thresholds = field(default_factory=Thresholds)

    # Paths to ignore
    ignore_paths: list[str] = field(
        default_factory=lambda: ["**/node_modules/**", "**/.venv/**", "**/vendor/**"]
    )

    @classmethod
    def from_yaml(cls, yaml_content: str) -> "RepoConfig":
        """Parse configuration from YAML string."""
        data = yaml.safe_load(yaml_content) or {}

        thresholds_data = data.pop("thresholds", {})
        thresholds = Thresholds(
            cyclomatic_complexity=thresholds_data.get("cyclomatic_complexity", 10),
            function_length=thresholds_data.get("function_length", 50),
            nesting_depth=thresholds_data.get("nesting_depth", 4),
        )

        return cls(
            scan_interval=data.get("scan_interval", "24h"),
            max_prs_per_day=data.get("max_prs_per_day", 3),
            test_command=data.get("test_command"),
            analyzers=data.get("analyzers", ["complexity", "type_hints", "duplicates"]),
            thresholds=thresholds,
            ignore_paths=data.get(
                "ignore_paths", ["**/node_modules/**", "**/.venv/**", "**/vendor/**"]
            ),
        )

    @classmethod
    def from_file(cls, path: Path) -> "RepoConfig":
        """Load configuration from a .mohtion.yaml file."""
        if not path.exists():
            return cls()  # Return defaults if no config file
        return cls.from_yaml(path.read_text())

    @classmethod
    def default(cls) -> "RepoConfig":
        """Return default configuration."""
        return cls()
