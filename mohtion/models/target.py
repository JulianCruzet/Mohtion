"""Tech debt target model."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class DebtType(str, Enum):
    """Types of technical debt that Mohtion can detect."""

    COMPLEXITY = "complexity"  # High cyclomatic complexity
    TYPE_HINTS = "type_hints"  # Missing type annotations
    DUPLICATE = "duplicate"  # Duplicate code blocks
    DEPRECATION = "deprecation"  # Deprecated API usage


@dataclass
class TechDebtTarget:
    """A specific piece of technical debt identified in the codebase."""

    file_path: Path
    start_line: int
    end_line: int
    debt_type: DebtType
    severity: float  # 0.0 to 1.0, higher = more severe
    description: str
    code_snippet: str  # The actual code that needs refactoring

    # Optional metadata
    function_name: str | None = None
    class_name: str | None = None
    metric_value: float | None = None  # e.g., cyclomatic complexity score

    @property
    def location(self) -> str:
        """Human-readable location string."""
        parts = [str(self.file_path)]
        if self.class_name:
            parts.append(self.class_name)
        if self.function_name:
            parts.append(self.function_name)
        return ":".join(parts) + f" (lines {self.start_line}-{self.end_line})"

    def __str__(self) -> str:
        return f"[{self.debt_type.value}] {self.location}: {self.description}"
