---
id: code_quality_standards
category: behavior
priority: 75
version: 1.0
description: >
  Establishes Spark’s foundational coding principles: type safety,
  public documentation, simplicity, readability, and maintainability.
  Guides code structure across all modules and assists in quality enforcement.
---

## Required Code Standards

- Type hints required for all functions and public APIs  
- All public-facing functions, classes, and modules must include docstrings  
- Functions must be focused and short—no excessive branching or nesting  
- Line length: 88 characters max  
- Code must follow **existing repo patterns** unless a proposal is discussed

## Development Philosophy

| Principle       | Summary                                           |
|-----------------|----------------------------------------------------|
| Simplicity      | Prioritize simple, clear, direct solutions         |
| Readability     | Code should speak for itself                       |
| Performance     | Improve performance only when it aids clarity      |
| Maintainability | Minimize future developer burden                   |
| Testability     | All code must be reasonably easy to test           |
| Reusability     | Modular, composable components over hardcoding     |

> Less Code = Less Debt. If it can be deleted, it's usually better.

## Style Enforcement

- Function and variable names: `snake_case`  
- Class names: `PascalCase`  
- Constants: `UPPER_SNAKE_CASE`  
- Use `f"` strings for formatting—avoid concatenation  
- Docstrings must be Google-style or PEP257-compliant

## Common Quality Gaps

- No type hints or `Any` types  
- Missing docstrings on shared modules  
- Large monolithic functions with multiple responsibilities  
- Violations of known patterns (e.g., repo-specific casing or file layout)  
- Unannotated side effects (e.g., logging, file writes)

## Anchor Comments

- Required in complex logic or unclear refactors  
- Format:
  - `AIDEV-NOTE:` for clarification  
  - `AIDEV-TODO:` for pending items  
  - `AIDEV-QUESTION:` for unresolved decisions  
- Never remove `AIDEV-*` anchors without developer approval  
- If modifying code adjacent to anchors, update comment accordingly

## File Hygiene Rules

- Match naming and structure of related modules  
- Limit scope: prefer multiple focused files over one bloated file  
- Maintain test co-location when feasible  
- Avoid “catch-all” files—split by purpose

## Pro Tips

- Build iteratively: validate each step before layering complexity  
- Use functional and stateless design when practical  
- Push implementation details to edges—keep core logic clean  
- When unsure:
  > “🧠 This logic touches multiple concerns—shall I flag and annotate?”

## Quality Audit Reminders

- Check:
  - `git status` before commit  
  - Run formatters and linters  
  - Verify test coverage  
  - Ensure type safety  
  - Document public APIs  
  - Review anchor comments  

## Golden Rule

> If it’s unclear—ask. If it’s clever—reconsider. If it’s simple—ship it.

