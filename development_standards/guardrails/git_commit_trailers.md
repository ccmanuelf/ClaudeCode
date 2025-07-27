---
id: git_commit_trailers
category: guardrail
priority: 50
version: 1.0
description: >
  Enforces commit message hygiene for traceability, reproducibility,
  and communication clarity. Establishes standardized trailer conventions
  and prohibits tool attribution in source control history.
---

## Required Trailers (When Applicable)

### For bug fixes or features reported by individuals:
```bash
git commit --trailer "Reported-by:<name>"
```
- `<name>` must match the submitter’s name or username  
- Trailer must be added via CLI or template—not interpolated automatically  
- This enables provenance tracking and acknowledgment

### For issues resolved from GitHub:
```bash
git commit --trailer "Github-Issue:#<number>"
```
- `<number>` corresponds to the actual GitHub issue  
- Trailer must appear at the end of commit message block  
- Use only the main issue number—avoid subthreads or crosslinks

## Forbidden Metadata

- ❌ Do NOT use:
  - `Co-authored-by:`  
  - `Generated-by:`  
  - `Tool:` attribution lines (e.g., "Created by ChatGPT", etc.)  
- ❌ Do not mention AI or assistant names in commit messages  
- ❌ Never auto-generate commit trailers without developer oversight

## Ethics of Attribution

> Attribution belongs to the team and human authors.  
> AI-generated components must be reviewed and approved before merging.

## Commit Etiquette

- Trailer lines must be clean and scoped  
- Do not overstuff messages with context—keep narrative in the PR description  
- Use trailers only for structured metadata—not storytelling  
- Example:
  ```plaintext
  Fix profile image upload bug
  
  Corrected MIME type handling in upload handler
  
  Reported-by:JaneDoe  
  Github-Issue:#82
  ```

## Enforcement

- Validate trailers via commit hooks or review checklist  
- Strip tool-related annotations before merge  
- If commit contains forbidden metadata:
  > “🛑 Please remove tool attribution from commit history before continuing.”

## Golden Rule

> 🧠 Developer context drives version history. Always ask before attributing content or modifying credit structures.
