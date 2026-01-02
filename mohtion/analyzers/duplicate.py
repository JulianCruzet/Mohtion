"Duplicate code analyzer using Python AST."

import ast
import hashlib
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

from mohtion.analyzers.base import Analyzer
from mohtion.models.repo_config import RepoConfig
from mohtion.models.target import DebtType, TechDebtTarget

logger = logging.getLogger(__name__)


class DuplicateVisitor(ast.NodeVisitor):
    """AST visitor that finds duplicate function bodies."""

    def __init__(self) -> None:
        self.blocks: list[dict[str, Any]] = []
        self._current_class: str | None = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Track current class context."""
        old_class = self._current_class
        self._current_class = node.name
        self.generic_visit(node)
        self._current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Analyze a function definition."""
        self._check_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Analyze an async function definition."""
        self._check_function(node)
        self.generic_visit(node)

    def _check_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        # We want to check if the logic (body) is identical
        if not node.body:
            return

        # Create a dummy module to hold the body so we can unparse it consistently
        # This handles indentation normalization automatically
        body_node = ast.Module(body=node.body, type_ignores=[])

        # Remove docstring if present (it's the first statement if it's a string constant)
        if (
            len(body_node.body) > 0
            and isinstance(body_node.body[0], ast.Expr)
            and isinstance(body_node.body[0].value, ast.Constant)
            and isinstance(body_node.body[0].value.value, str)
        ):
            body_node.body = body_node.body[1:]

        try:
            # unparse() produces canonical code representation
            normalized_code = ast.unparse(body_node).strip()
        except Exception:
            # Fallback for complex ASTs that might fail unparse
            return

        # Skip trivial functions (empty, pass, or too short)
        if not normalized_code or normalized_code == "pass":
            return
        
        # Heuristic: Skip functions with fewer than 3 lines of logic
        # (reduces noise from simple getters/setters/wrappers)
        if len(normalized_code.splitlines()) < 3:
            return

        code_hash = hashlib.md5(normalized_code.encode("utf-8")).hexdigest()

        self.blocks.append({
            "name": node.name,
            "class_name": self._current_class,
            "start_line": node.lineno,
            "end_line": node.end_lineno or node.lineno,
            "hash": code_hash,
            "code": normalized_code,
            "node": node
        })


class DuplicateAnalyzer(Analyzer):
    """Analyzer for identifying duplicate code blocks within a file."""

    @property
    def name(self) -> str:
        return "duplicates"

    async def analyze_file(self, file_path: Path, content: str) -> list[TechDebtTarget]:
        """Analyze a Python file for duplicate code."""
        # Only analyze Python files
        if file_path.suffix != ".py":
            return []

        if not self.should_analyze(file_path):
            return []

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logger.warning(f"Failed to parse {file_path}: {e}")
            return []

        visitor = DuplicateVisitor()
        visitor.visit(tree)

        # Group by hash
        hash_groups = defaultdict(list)
        for block in visitor.blocks:
            hash_groups[block["hash"]].append(block)

        targets = []
        lines = content.split("\n")

        for code_hash, group in hash_groups.items():
            if len(group) > 1:
                # Found duplicates!
                # We create a target for each instance, referencing the others
                
                # Sort group by line number
                group.sort(key=lambda x: x["start_line"])
                
                for i, block in enumerate(group):
                    # Find the "original" (first occurrence) to reference
                    original = group[0]
                    is_original = (i == 0)
                    
                    # If it's the original, we might still want to flag it if there are copies
                    # But usually we want to flag the COPIES to be removed/refactored.
                    # Actually, refactoring strategy is "Extract Method".
                    # So we should flag ALL of them so the agent sees the full picture.
                    
                    other_locations = [
                        f"{b['name']} (line {b['start_line']})" 
                        for j, b in enumerate(group) if i != j
                    ]
                    
                    description = (
                        f"Duplicate code logic found. "
                        f"Identical to {', '.join(other_locations)}."
                    )
                    
                    # Extract code
                    start = block["start_line"] - 1
                    end = block["end_line"]
                    code_snippet = "\n".join(lines[start:end])
                    
                    # Severity calculation
                    # Longer duplicates = higher severity
                    # More copies = higher severity
                    lines_of_code = len(block["code"].splitlines())
                    base_severity = min(1.0, lines_of_code / 20) # 20 lines = 1.0
                    multiplier = 1.0 + (0.1 * (len(group) - 1))
                    severity = min(1.0, base_severity * multiplier)

                    target = TechDebtTarget(
                        file_path=file_path,
                        start_line=block["start_line"],
                        end_line=block["end_line"],
                        debt_type=DebtType.DUPLICATE,
                        severity=severity,
                        description=description,
                        code_snippet=code_snippet,
                        function_name=block["name"],
                        class_name=block["class_name"],
                        metric_value=float(len(group)), # Metric = count of duplicates
                    )
                    targets.append(target)

        return targets
