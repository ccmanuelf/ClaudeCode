---
id: coding_best_practices
category: behavior
priority: 70
version: 1.0
description: >
  Guides Spark’s coding approach toward simplicity, clarity, maintainability,
  and developer empathy. Enforces naming discipline, structural hygiene,
  iterative build habits, and functional design principles.
---

## Core Practices

### 🧭 Early Returns  
- Use to eliminate nested conditionals  
- Improves readability and short-circuits logic cleanly  
- Example:
  ```python
  if not user:
      return None
  ```

### 🔤 Descriptive Naming  
- Use clear names for variables, functions, and classes  
- Handlers should start with `handle_`, filters with `filter_`  
- Avoid abbreviations unless common (e.g., `id`, `url`)  
- Prefer `user_profile_picture` over `upp`

### 📛 Constants Over Functions  
- If a value doesn’t change, make it a constant  
- Place constants at top of file  
- Name in `UPPER_SNAKE_CASE`

### 🧱 DRY Principle  
- “Don’t Repeat Yourself” applies across files  
- Abstract repeated logic into helpers  
- Consolidate config fragments and payload templates

### 🧪 Functional Style  
- Prefer stateless, pure functions when possible  
- Avoid side effects unless scoped  
- Compose behavior from small, focused building blocks

### 🧩 Minimal Change Philosophy  
- Modify only code related to the task at hand  
- Avoid sweeping reformatting, refactors, or deletions without scoped intent  
- Track changes deliberately—one purpose per commit

### 🔃 Function Ordering  
- Define composing functions before their components  
- Improves readability and top-down flow  
- Example: `create_response()` before `generate_payload()`

### 📝 TODO Comments  
- Mark known issues or gaps using:
  ```python
  # TODO: Add fallback for empty user_id
  ```  
- Use `AIDEV-TODO:` when signaling AI-related resolution needs

## Build Strategy

### 🔁 Build Iteratively  
- Validate core function before adding logic  
- Start minimal, test, then layer complexity  
- Don’t optimize prematurely

### 🧪 Run Tests Frequently  
- Validate code with realistic inputs  
- Recheck outputs before commit  
- Use CI or local runners as sanity gate

### 🧪 Create Test Environments  
- For hard-to-validate components, isolate logic  
- Mock external services, user data, configs  
- Explain mock logic via comments or anchor notes

## Functional Code Principles

- Use data transformations that avoid mutation  
- Compose behavior via pipelines and helpers  
- Push implementation details to the edges—keep core logic clean

## File Organization

- Structure files by domain or behavior  
- Avoid catch-all utils—split helpers by concern  
- Keep number of files proportional to project scale

## Philosophy Recap

> Simple is beautiful.  
> Readable is reliable.  
> Minimalism helps maintainability.  
> Helpful comments are empathy in code form.
