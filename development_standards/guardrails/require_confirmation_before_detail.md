---
id: require_confirmation_before_detail
category: guardrail
priority: 85
version: 1.0
description: >
  Prevents the assistant from generating detailed subtasks or implementation suggestions
  without explicit user confirmation (e.g., 'Go', 'Yes', or 'Proceed').
---

## Rule

Do not proceed to subtask elaboration, file creation suggestions, or technical breakdowns
until the user has replied with an affirmative signal.

## Accepted Signals

- "Go"  
- "Yes"  
- "Y"  
- "Proceed"  
- "Continue"

## Rationale

This ensures user control during task list development, prevents overreach,
and gives the user space to review and reflect before moving forward.

## Enforcement

- Always pause after listing parent tasks  
- Use `prompts/task_list_interactions.md` to elicit the next step  
- If no confirmation is received, halt and await input  
