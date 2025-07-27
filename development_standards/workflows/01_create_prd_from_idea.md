---
id: create_prd
category: workflow
priority: 40
version: 1.0
description: >
  Assist beginner developers in ideating and generating a PRD.md file
  using conversational clarification and structured questioning.
---

## Purpose

Help users transform raw ideas into structured PRD documents by
guiding them through thoughtful questioning, summarization, and template injection.

## Process

1. Begin with a friendly intro and explain the plan.  
2. Ask clarifying questions (one at a time).  
   - Use prompts from `prompts/prd_question_framework.md`  
3. Summarize understanding periodically to confirm direction.  
4. Provide technology recommendations (conceptual only).  
5. Generate PRD using `templates/prd_structure_template.json`.  
6. Save document as: `/tasks/prd-[project-name]-[date].md`.

## Constraints

- No code generation allowed.  
- Must use filesystem if available; otherwise, respond in chat.  
- Prioritize tools (`Brave`, `Tavily`) when enabled.
