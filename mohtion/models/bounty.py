"""Bounty result model - tracks the outcome of a refactoring attempt."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from mohtion.models.target import TechDebtTarget


class BountyStatus(str, Enum):
    """Status of a bounty (refactoring attempt)."""

    PENDING = "pending"  # Not yet started
    IN_PROGRESS = "in_progress"  # Currently being processed
    TESTING = "testing"  # Running tests
    RETRYING = "retrying"  # Tests failed, attempting self-heal
    SUCCESS = "success"  # PR opened successfully
    FAILED = "failed"  # Failed after max retries
    ABANDONED = "abandoned"  # Gave up (e.g., tests still fail)


@dataclass
class BountyResult:
    """Result of attempting to fix a tech debt target."""

    target: TechDebtTarget
    status: BountyStatus
    branch_name: str

    # Timestamps
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None

    # Results
    pr_url: str | None = None
    pr_number: int | None = None

    # Refactoring details
    original_code: str = ""
    refactored_code: str = ""
    refactoring_summary: str = ""

    # Test execution
    test_passed: bool = False
    test_output: str = ""
    retry_count: int = 0

    # Error tracking
    error_message: str | None = None

    def mark_success(self, pr_url: str, pr_number: int) -> None:
        """Mark the bounty as successfully completed."""
        self.status = BountyStatus.SUCCESS
        self.pr_url = pr_url
        self.pr_number = pr_number
        self.test_passed = True
        self.completed_at = datetime.utcnow()

    def mark_failed(self, error: str) -> None:
        """Mark the bounty as failed."""
        self.status = BountyStatus.FAILED
        self.error_message = error
        self.completed_at = datetime.utcnow()

    def __str__(self) -> str:
        status_icon = {
            BountyStatus.SUCCESS: "✓",
            BountyStatus.FAILED: "✗",
            BountyStatus.IN_PROGRESS: "⋯",
            BountyStatus.TESTING: "🧪",
            BountyStatus.RETRYING: "↻",
        }.get(self.status, "?")
        return f"{status_icon} {self.target.location} [{self.status.value}]"
