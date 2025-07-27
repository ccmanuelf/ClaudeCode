---
id: task_execution_protocol
category: guardrail
priority: 80
version: 1.0
description: >
  Governs how the AI assistant progresses through generated task lists,
  requiring user confirmation and maintaining synchronized file updates.
---

## Execution Rules

- Do not begin the next subtask until the user responds with "Yes", "Y", or "Go".
- After completing a subtask, mark it as `[x]` and pause for confirmation.
- If all subtasks under a parent are complete, mark the parent task as `[x]`.

## File Maintenance Protocol

1. Update the task list file after each confirmed subtask is completed.  
2. Maintain a “Relevant Files” section with:
   - All created or modified files
   - One-line purpose descriptions
3. Add new tasks if implementation reveals missing coverage.

## Interaction Loop

- Start: identify the next `Pending` subtask.  
- Ask user: "Shall I begin work on [subtask description]?"  
- On confirmation: proceed, then mark `[x]`  
- Ask user: "Shall we continue to the next item?"

## Edge Cases

- If a task is ambiguous, pause and ask for clarification  
- If a subtask becomes blocked, annotate and halt progression  
- If the user pauses execution, maintain current state and await input

## Visual Syntax Enforcement

Follow the notation defined in `behaviors/task_lifecycle.md` for task state icons and indicators.
