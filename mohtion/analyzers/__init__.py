"""Code analyzers for tech debt detection."""

from mohtion.analyzers.base import Analyzer
from mohtion.analyzers.complexity import ComplexityAnalyzer

__all__ = ["Analyzer", "ComplexityAnalyzer"]
