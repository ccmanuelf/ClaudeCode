---
id: testing_and_refactor_guidelines
category: behavior
priority: 70
version: 1.0
description: >
  Outlines best practices for implementing tests, conducting refactors, and
  maintaining system integrity. Ensures sustainable, readable, and safe evolution
  of code across Spark-supported workflows.
---

## Refactor Triggers

- Duplicate logic across files or modules  
- Fragile conditionals or nested structures  
- Repetitive constants or magic strings  
- Poor test coverage or difficult-to-test code  
- Violation of naming or style conventions  
- Performance bottlenecks without clarity loss

## Refactor Workflow

1. Identify logical grouping or reusable pattern  
2. Define new abstraction without side effects  
3. Migrate related code incrementally  
4. Maintain original API contracts  
5. Add/refactor tests before merge  
6. Preserve anchor comments if relevant

## Testing Checklist (Before Finalizing)

- ✅ All new logic has coverage  
- ✅ Lint passes recursively (`lint --recursive`)  
- ✅ Variable references resolved  
- ✅ Outputs tested for real & mocked data  
- ✅ Behavior validated under edge cases  
- ✅ Documentation updated  
- ✅ Anchor comments added for risky logic

## Mock vs Real Data Testing

| Condition                     | Approach                  |
|-------------------------------|---------------------------|
| External API unavailable      | Use rich mocks            |
| Sensitive or protected data   | Use synthetic payloads    |
| Simple transformation logic   | Use real examples         |
| High side-effect risk         | Isolate in test harness   |

Always explain mocked data structure and assumptions. Use comment like:
```python
# AIDEV-NOTE: Using mock payload as auth server is unavailable in CI
```

## Structural Guidelines

- Place test files alongside implementation  
- Use modular fixtures and helpers  
- Prefer reusable test blocks over duplication  
- Respect naming symmetry (`Feature → Feature.test.ts`)

## Refactor Etiquette

- Never refactor tests to change expected behavior  
- Never mutate tests to pass new logic—write fresh ones  
- Confirm with developer if test change introduces risk  
- Annotate significant changes with:
  ```python
  # AIDEV-TODO: Verify this new logic handles legacy inputs
  ```

## Common Mistakes to Avoid

- Refactoring without tests  
- Optimizing obscure logic at readability cost  
- Removing comments that explain edge cases  
- Skipping validation for modified dependencies  
- Renaming without checking downstream references

## Philosophy

> 📐 Refactor small. Test thoroughly. Comment generously.  
> The future depends on what you leave behind for others to trust.
