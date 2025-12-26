"""Refactor - Action phase of the agent loop."""

import logging
from dataclasses import dataclass
from pathlib import Path

from mohtion.llm.client import LLMClient
from mohtion.models.target import TechDebtTarget

logger = logging.getLogger(__name__)


@dataclass
class RefactorResult:
    """Result of a refactoring attempt."""

    success: bool
    original_code: str
    refactored_code: str
    summary: str
    error: str | None = None


class Refactor:
    """Handles code refactoring using LLM."""

    def __init__(self, repo_path: Path) -> None:
        self.repo_path = repo_path
        self.llm = LLMClient()

    async def refactor_target(self, target: TechDebtTarget) -> RefactorResult:
        """
        Refactor a tech debt target.

        Args:
            target: The tech debt target to refactor

        Returns:
            RefactorResult with the refactored code
        """
        logger.info(f"Refactoring {target.location}")

        try:
            refactored_code, summary = await self.llm.refactor_code(
                code=target.code_snippet,
                debt_description=target.description,
                file_path=str(target.file_path),
                function_name=target.function_name,
            )

            return RefactorResult(
                success=True,
                original_code=target.code_snippet,
                refactored_code=refactored_code,
                summary=summary,
            )

        except Exception as e:
            logger.exception(f"Refactoring failed for {target.location}")
            return RefactorResult(
                success=False,
                original_code=target.code_snippet,
                refactored_code="",
                summary="",
                error=str(e),
            )

    async def apply_refactoring(
        self, target: TechDebtTarget, refactored_code: str
    ) -> bool:
        """
        Apply refactored code to the file.

        Args:
            target: The original tech debt target
            refactored_code: The refactored code to apply

        Returns:
            True if successful, False otherwise
        """
        file_path = self.repo_path / target.file_path

        try:
            # Read the full file
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Replace the target lines with refactored code
            start = target.start_line - 1
            end = target.end_line
            refactored_lines = refactored_code.split("\n")

            new_lines = lines[:start] + refactored_lines + lines[end:]
            new_content = "\n".join(new_lines)

            # Write back
            file_path.write_text(new_content, encoding="utf-8")
            logger.info(f"Applied refactoring to {target.file_path}")
            return True

        except Exception as e:
            logger.exception(f"Failed to apply refactoring: {e}")
            return False

    async def attempt_self_heal(
        self,
        target: TechDebtTarget,
        refactored_code: str,
        test_output: str,
    ) -> RefactorResult:
        """
        Attempt to fix a failed refactoring based on test output.

        Args:
            target: The original tech debt target
            refactored_code: The refactored code that failed tests
            test_output: The test failure output

        Returns:
            RefactorResult with the fixed code
        """
        logger.info(f"Attempting self-heal for {target.location}")

        try:
            fixed_code, explanation = await self.llm.analyze_test_error(
                original_code=target.code_snippet,
                refactored_code=refactored_code,
                test_output=test_output,
            )

            return RefactorResult(
                success=True,
                original_code=target.code_snippet,
                refactored_code=fixed_code,
                summary=f"Self-heal: {explanation}",
            )

        except Exception as e:
            logger.exception("Self-heal failed")
            return RefactorResult(
                success=False,
                original_code=target.code_snippet,
                refactored_code=refactored_code,
                summary="",
                error=str(e),
            )
