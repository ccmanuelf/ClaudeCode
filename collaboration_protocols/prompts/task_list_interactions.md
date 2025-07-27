---
id: task_list_interactions
category: prompt
priority: 25
version: 1.0
description: >
  Reusable conversational prompts for generating and confirming implementation task lists
  from PRD documents, supporting user approval flow.
---

## Task List Generation Prompts

- "Based on your PRD, I've generated a set of high-level tasks. Let me know when you're ready to break them down into actionable subtasks—just say 'Go'."
- "Here are the subtasks derived from each parent item. Want to refine or expand anything before we proceed?"
- "Would you like me to suggest which files will be created or modified in this implementation?"

## Task Confirmation Prompts

- "Subtasks are complete. Ready for me to assemble the final task list output?"
- "Shall I continue to the next parent task? You can reply with 'Yes', 'Y', or 'Go ahead'."
- "Paused as requested. Just let me know when you're ready to move forward."

## Tone & Constraints

- Keep all prompts friendly and clear  
- Do not use technical jargon unless requested  
- Always seek explicit confirmation before continuing task breakdown or committing output
