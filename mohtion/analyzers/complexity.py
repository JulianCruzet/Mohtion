"""Cyclomatic complexity analyzer using Python AST."""

import ast
import logging
from pathlib import Path

from mohtion.analyzers.base import Analyzer
from mohtion.models.repo_config import RepoConfig
from mohtion.models.target import DebtType, TechDebtTarget

logger = logging.getLogger(__name__)


class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor that calculates cyclomatic complexity."""

    def __init__(self) -> None:
        self.functions: list[dict] = []
        self._current_class: str | None = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Track current class context."""
        old_class = self._current_class
        self._current_class = node.name
        self.generic_visit(node)
        self._current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Analyze a function definition."""
        complexity = self._calculate_complexity(node)
        self.functions.append({
            "name": node.name,
            "class_name": self._current_class,
            "start_line": node.lineno,
            "end_line": node.end_lineno or node.lineno,
            "complexity": complexity,
        })
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def _calculate_complexity(self, node: ast.AST) -> int:
        """
        Calculate cyclomatic complexity of a node.

        Complexity = 1 + number of decision points
        Decision points: if, elif, for, while, except, and, or, ternary
        """
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            # Branching statements
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            # Exception handlers
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            # Boolean operators (each adds a decision point)
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            # Ternary expressions
            elif isinstance(child, ast.IfExp):
                complexity += 1
            # Comprehensions with conditions
            elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                for generator in child.generators:
                    complexity += len(generator.ifs)
            # Assert statements
            elif isinstance(child, ast.Assert):
                complexity += 1

        return complexity


class ComplexityAnalyzer(Analyzer):
    """Analyzer for cyclomatic complexity in Python files."""

    @property
    def name(self) -> str:
        return "complexity"

    def __init__(self, config: RepoConfig) -> None:
        super().__init__(config)
        self.threshold = config.thresholds.cyclomatic_complexity

    async def analyze_file(self, file_path: Path, content: str) -> list[TechDebtTarget]:
        """Analyze a Python file for high-complexity functions."""
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

        visitor = ComplexityVisitor()
        visitor.visit(tree)

        targets = []
        lines = content.split("\n")

        for func in visitor.functions:
            if func["complexity"] > self.threshold:
                # Extract the function code
                start = func["start_line"] - 1
                end = func["end_line"]
                code_snippet = "\n".join(lines[start:end])

                # Calculate severity (normalize complexity above threshold)
                severity = min(1.0, (func["complexity"] - self.threshold) / 10)

                target = TechDebtTarget(
                    file_path=file_path,
                    start_line=func["start_line"],
                    end_line=func["end_line"],
                    debt_type=DebtType.COMPLEXITY,
                    severity=severity,
                    description=f"High cyclomatic complexity: {func['complexity']} (threshold: {self.threshold})",
                    code_snippet=code_snippet,
                    function_name=func["name"],
                    class_name=func["class_name"],
                    metric_value=float(func["complexity"]),
                )
                targets.append(target)

        return targets
