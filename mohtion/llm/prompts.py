"""Prompt templates for LLM operations."""

REFACTOR_PROMPT = """You are an expert code refactoring assistant. Your task is to refactor the following code to address the identified technical debt.

{context}

## Technical Debt Issue
{debt_description}

## Original Code
```
{code}
```

## Requirements
1. Refactor the code to fix the identified issue
2. Preserve the exact same external behavior and API
3. Do not change function signatures or return types
4. Improve readability and maintainability
5. Keep the refactoring minimal and focused

## Response Format
Provide the refactored code in a code block, followed by a brief summary of changes.

```python
# Your refactored code here
```

Summary: Briefly describe what you changed and why.
"""

ANALYZE_ERROR_PROMPT = """You are an expert debugging assistant. A code refactoring caused tests to fail. Analyze the error and fix the refactored code.

## Original Code (working)
```
{original_code}
```

## Refactored Code (broken)
```
{refactored_code}
```

## Test Failure Output
```
{test_output}
```

## Task
1. Analyze why the refactored code broke the tests
2. Fix the refactored code while still addressing the original tech debt
3. Ensure the fix maintains the same behavior as the original

## Response Format
Provide the fixed code in a code block, followed by an explanation.

```python
# Your fixed code here
```

Explanation: What was wrong and how you fixed it.
"""

VIBE_CHECK_PROMPT = """You are a code quality analyst. Review this code and identify potential issues.

## Code
```{language}
{code}
```

## Analysis Request
Look for:
1. Code smells (long methods, deep nesting, unclear naming)
2. Potential bugs or edge cases
3. Missing error handling
4. Opportunities for simplification

Rate the overall code quality from 1-10 and list specific issues if any.

Respond in this format:
Quality Score: X/10
Issues:
- Issue 1: description
- Issue 2: description
(or "None found" if the code is clean)
"""
