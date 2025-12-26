"""Claude LLM client for code analysis and refactoring."""

import logging

import anthropic

from mohtion.config import get_settings
from mohtion.llm.prompts import (
    ANALYZE_ERROR_PROMPT,
    REFACTOR_PROMPT,
)

logger = logging.getLogger(__name__)


class LLMClient:
    """Claude API client for Mohtion operations."""

    MODEL = "claude-sonnet-4-20250514"
    MAX_TOKENS = 4096

    def __init__(self) -> None:
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def refactor_code(
        self,
        code: str,
        debt_description: str,
        file_path: str,
        function_name: str | None = None,
    ) -> tuple[str, str]:
        """
        Refactor code to fix identified tech debt.

        Args:
            code: The original code to refactor
            debt_description: Description of the tech debt issue
            file_path: Path to the file being refactored
            function_name: Name of the function (if applicable)

        Returns:
            Tuple of (refactored_code, summary_of_changes)
        """
        context = f"File: {file_path}"
        if function_name:
            context += f"\nFunction: {function_name}"

        prompt = REFACTOR_PROMPT.format(
            context=context,
            debt_description=debt_description,
            code=code,
        )

        logger.debug(f"Requesting refactor for {file_path}")

        # Use sync client in async context (anthropic handles this)
        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=self.MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse response - expecting code block and summary
        content = response.content[0].text
        return self._parse_refactor_response(content)

    def _parse_refactor_response(self, content: str) -> tuple[str, str]:
        """Parse LLM response into code and summary."""
        # Look for code block
        if "```" in content:
            parts = content.split("```")
            # Find the code block (skip language identifier if present)
            code_block = ""
            summary = ""

            for i, part in enumerate(parts):
                if i % 2 == 1:  # Odd indices are inside code blocks
                    # Remove language identifier from first line if present
                    lines = part.strip().split("\n")
                    if lines and lines[0] in ("python", "py", "javascript", "js", "typescript", "ts"):
                        code_block = "\n".join(lines[1:])
                    else:
                        code_block = part.strip()
                elif i > 0:  # Text after code block
                    summary += part.strip()

            if not summary:
                summary = "Code refactored to reduce complexity."

            return code_block, summary.strip()

        # No code block found - return as-is with generic summary
        return content.strip(), "Code refactored."

    async def analyze_test_error(
        self,
        original_code: str,
        refactored_code: str,
        test_output: str,
    ) -> tuple[str, str]:
        """
        Analyze test failure and suggest a fix.

        Args:
            original_code: The original code before refactoring
            refactored_code: The refactored code that caused test failure
            test_output: The test failure output/logs

        Returns:
            Tuple of (fixed_code, explanation)
        """
        prompt = ANALYZE_ERROR_PROMPT.format(
            original_code=original_code,
            refactored_code=refactored_code,
            test_output=test_output,
        )

        logger.debug("Requesting error analysis for self-healing")

        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=self.MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.content[0].text
        return self._parse_refactor_response(content)
