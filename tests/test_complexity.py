"""Tests for the complexity analyzer."""

import pytest

from mohtion.analyzers.complexity import ComplexityAnalyzer
from mohtion.models.repo_config import RepoConfig
from mohtion.models.target import DebtType
from pathlib import Path


@pytest.fixture
def analyzer() -> ComplexityAnalyzer:
    config = RepoConfig()
    config.thresholds.cyclomatic_complexity = 5  # Lower threshold for testing
    return ComplexityAnalyzer(config)


@pytest.mark.asyncio
async def test_simple_function_no_debt(analyzer: ComplexityAnalyzer) -> None:
    """Simple functions should not be flagged."""
    code = '''
def simple_add(a, b):
    return a + b
'''
    targets = await analyzer.analyze_file(Path("test.py"), code)
    assert len(targets) == 0


@pytest.mark.asyncio
async def test_complex_function_detected(analyzer: ComplexityAnalyzer) -> None:
    """Complex functions should be flagged."""
    code = '''
def complex_function(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                return x + y + z
            else:
                return x + y
        else:
            if z > 0:
                return x + z
            else:
                return x
    else:
        if y > 0:
            return y
        else:
            return 0
'''
    targets = await analyzer.analyze_file(Path("test.py"), code)
    assert len(targets) == 1
    assert targets[0].debt_type == DebtType.COMPLEXITY
    assert targets[0].function_name == "complex_function"


@pytest.mark.asyncio
async def test_ignores_non_python(analyzer: ComplexityAnalyzer) -> None:
    """Non-Python files should be ignored."""
    code = "function test() { return 1; }"
    targets = await analyzer.analyze_file(Path("test.js"), code)
    assert len(targets) == 0


@pytest.mark.asyncio
async def test_handles_syntax_errors(analyzer: ComplexityAnalyzer) -> None:
    """Syntax errors should be handled gracefully."""
    code = "def broken( { return"
    targets = await analyzer.analyze_file(Path("test.py"), code)
    assert len(targets) == 0
