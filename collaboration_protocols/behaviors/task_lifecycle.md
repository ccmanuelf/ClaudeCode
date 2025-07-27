---
id: task_lifecycle
category: behavior
priority: 50
version: 1.0
description: >
  Defines the state machine and progression logic for AI-generated tasks
  during execution, including transition rules and status indicators.
---

## Allowed Task States

- `Pending` – Not yet started  
- `In Progress` – Actively being worked on  
- `Blocked` – Cannot proceed due to external issue or dependency  
- `Completed` – Successfully finished  
- `Cancelled` – Task was terminated by user or system decision

## State Transition Logic

| From         | To             | Trigger                       |
|--------------|----------------|-------------------------------|
| Pending      | In Progress    | User confirms task start      |
| In Progress  | Completed      | AI confirms all criteria met  |
| In Progress  | Blocked        | AI identifies blocking issue  |
| Any          | Cancelled      | Explicit cancellation command |

## Markdown Syntax for Visual Tracking

- `- [ ]` = Pending  
- `- [x]` = Completed  
- `- [ ] 🚧` = In Progress  
- `- [ ] 🔒` = Blocked  
- `- [ ] ❌` = Cancelled

## Status Indicators

AI may append status notes next to task lines when relevant:

- `// blocked by unmet API dependency`  
- `// cancelled per user instruction`

## Enforcement Guidelines

- Never skip transitions without user input  
- Always annotate blocked/cancelled tasks with rationale  
- Maintain consistent visual cues for traceability
