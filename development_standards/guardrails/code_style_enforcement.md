---
id: code_style_enforcement
category: guardrail
priority: 55
version: 1.0
description: >
  Enforces coding standards, naming conventions, type hint requirements,
  docstring presence, formatting boundaries, and consistency across modules.
---

## Naming Conventions

| Element Type  | Style               | Example                          |
|---------------|---------------------|----------------------------------|
| Function      | `snake_case`        | `get_user_data()`                |
| Variable      | `snake_case`        | `profile_picture_url`            |
| Class         | `PascalCase`        | `UserProfileForm`                |
| Constants     | `UPPER_SNAKE_CASE`  | `MAX_ATTEMPTS = 5`               |
| Formatting    | f-string only       | `f"Welcome, {name}!"`            |

## Type Hint Requirements

- All functions must include explicit type hints  
- Return types must be declared  
- Optional or union types must be properly narrowed  
- Example:
  ```python
  def get_username(user_id: str) -> Optional[str]:
      ...
  ```

## Docstring Requirements

- Public APIs, classes, and exported modules **must** include docstrings  
- Use Google-style or PEP257-compliant format  
- Example:
  ```python
  def fetch_data():
      """Fetches user data from the primary API source."""
  ```

## Line Length Enforcement

- Maximum: **88 characters per line**  
- Break lines using parentheses or continuation syntax  
- Multi-line function calls should indent cleanly  
- Split long import statements with backslash or multiple lines

## Pattern Consistency

- Follow existing repo/module patterns exactly  
- Match formatting, ordering, and linting behavior  
- Do not introduce new styles without consensus

## Special Comment Anchors

- Use `AIDEV-NOTE:` for explanatory comments  
- Use `AIDEV-TODO:` for unresolved tasks  
- Use `AIDEV-QUESTION:` for implementation uncertainties  
- **Never remove anchor comments unless explicitly instructed by a developer**  
- Always scan files for existing anchors before making changes

## Public Commit Hygiene

- Avoid cleverness—default to clarity  
- Prefer descriptive names, readable logic  
- Apply golden rule:
  > “If it feels unclear, ask first.”

## Common Style Mistakes to Avoid

- Forgetting type hints  
- Docstring omission  
- Long lines without breaks  
- Unclear variable/function names  
- Mixing styles across modules  
- Inconsistent ordering of imports, decorators, and function bodies

## Review Phrase Prompt

> “🧹 Running style check... Line length, naming, type hints, and docstrings all validated. Clean and consistent.”
