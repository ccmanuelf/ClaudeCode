---
id: testing_protocols
category: behavior
priority: 65
version: 1.0
description: >
  Defines Spark’s testing strategy and expectations across all development workflows.
  Enforces coverage for edge cases, regression protection, mock vs real data handling,
  and async testing best practices.
---

## Testing Expectations by Change Type

| Change Type       | Required Tests                   |
|-------------------|----------------------------------|
| New Feature       | Unit + Integration + Edge Cases  |
| Bug Fix           | Regression Test + Boundary Check |
| Refactor          | No regression allowed            |
| Config Change     | Snapshot + Behavior Recheck      |
| API Addition      | Contract Test + Auth Verification|

## Coverage Requirements

- Cover both success and failure paths  
- Explicitly test edge cases: nulls, boundaries, bad inputs  
- Verify output formats and data persistence behavior  
- Document known gaps with:
  ```python
  # AIDEV-TODO: Add test for empty payload case
  ```

## Async Testing Policy

- Preferred Framework: `anyio` over `asyncio`  
- Rationale:
  - `anyio` supports structured concurrency and unified APIs  
  - Reduces flake risk in multithreaded environments  
- If `asyncio` is used, prompt developer with:
  > “Would you prefer switching to `anyio` for async tests?”

## Mock Data Guidelines

- Use mocked data only when real data is unavailable or risky  
- Mark mock-based tests explicitly in title or comment  
- Explain mock structure and assumptions  
- Prefer realism over minimalism when mocking complex flows

## Real Data Testing

- Run tests with realistic payloads when safe  
- Validate data ingestion, output shape, and persistence  
- Use validation steps tied to real DB/API calls if feasible

## Test Structure Rules

- Place tests in mirrored file structure (e.g., `file.py` → `file.test.py`)  
- Isolate independent tests from fragile mocks  
- Co-locate fixtures if reused across multiple test groups  
- Use `pytest` unless project mandates alternative

## Failure Handling

- On CI failure:
  - Fix order: formatting → type → lint → logic  
  - Annotate fix rationale in PR  
  - Never mutate tests just to make them pass

## Common Pitfalls to Avoid

- Testing only success paths  
- Not asserting output structure  
- Ignoring invalid input behavior  
- Assuming correct state without verification  
- Using `print()` instead of assertions  
- Skipping authentication or permission checks

## Golden Rule

> 📐 Every change deserves a test.  
> If you’re unsure how to test it, flag with `AIDEV-QUESTION:` for review.
