---
id: aidev_anchor_comments_policy
category: guardrail
priority: 75
version: 1.0
description: >
  Defines the usage, preservation, scanning, and update rules for AIDEV anchor comments
  throughout the codebase. Ensures inline knowledge persistence and respectful developer-AI communication.
---

## Purpose

Anchor comments serve as structured signals between developers and AI assistants.  
They encode intent, uncertainty, complexity, or warnings and must be treated with care.

## Accepted Anchor Formats

| Prefix              | Description                                |
|---------------------|--------------------------------------------|
| `AIDEV-NOTE:`       | Developer-oriented context or explanation  |
| `AIDEV-TODO:`       | Unfinished tasks or known gaps             |
| `AIDEV-QUESTION:`   | Uncertainty or inquiry for discussion      |

Example:
```python
# AIDEV-NOTE: This query assumes non-null user_id but may fail in edge cases
```

## Anchor Enforcement Rules

- ✅ Always scan file for `AIDEV-*` before modifying content  
- ✅ Do not delete or overwrite anchor comments without explicit user instruction  
- ✅ When modifying related code, update associated anchors  
- ✅ If no anchor exists but the code is complex/confusing → Add one

## Trigger Conditions for Anchor Creation

Create or update an anchor when:

- File contains dense logic or fragile patterns  
- Commented code is unclear, error-prone, or subjective  
- Change introduces uncertainty, edge case, or risk  
- Developer leaves relevant context in past interactions

## Anchor Handling During PR

- Highlight anchor comments in commit or PR description  
- Do not remove anchor trails without comment thread  
- Confirm with developer before altering anchor state  
- If anchor conflicts with logic:
  > “⚠️ Anchor suggests ambiguity. Would you like to revisit this assumption?”

## Special AI Behavior

- Anchor comments are considered protected knowledge artifacts  
- Must be propagated during reasoning, refactoring, or documentation  
- Treat anchors as inline memory for coordination and safety

## Commit Hygiene

If modifying a file with anchors:
```plaintext
📎 Anchor present: `AIDEV-NOTE`  
✅ Status: Updated for new logic  
🧠 Reminder: Anchor signals need manual review before removal
```

## Golden Rule

> 🧭 Never remove or ignore anchors unless explicitly permitted.  
> They are signposts for collaboration and safety between humans and AI.
