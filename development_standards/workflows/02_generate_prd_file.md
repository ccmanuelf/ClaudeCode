<!-- File: workflows/01_generate_prd.md -->
---
id: generate_prd
category: workflow
priority: 20
version: 1.0
description: >
  Elicit detail and output a clear, junior-developer-friendly
  Product Requirements Document (PRD) in Markdown.
---

## Purpose

Guide the AI assistant through a structured sequence of clarifications
and PRD generation steps to produce an actionable spec for a junior developer.

## Process

1. Receive the initial feature prompt from the user.  
2. Ask clarifying questions  
   - See prompts/clarify_prd_questions.md for question templates.  
3. Generate the PRD  
   - Use templates/prd_skeleton.json as the Markdown skeleton.  
4. Save the document  
   - Filename: `/tasks/prd-[feature-name].md`

## Clarifying Questions

Refer to `prompts/clarify_prd_questions.md` for dynamic question sets covering:

- Problem/Goal  
- Target User  
- Core Functionality  
- User Stories  
- Acceptance Criteria  
- Scope/Boundaries  
- Data Requirements  
- Design/UI Constraints  
- Edge Cases  
- Development Stack (language, frameworks, version)

## PRD Structure

1. **Introduction/Overview**  
2. **Goals**  
3. **User Stories**  
4. **Functional Requirements**  
5. **Non-Goals (Out of Scope)**  
6. **Design Considerations (Optional)**  
7. **Technical Considerations (Optional)**  
8. **Success Metrics**  
9. **Open Questions**

## Final Instructions

- Do not begin implementation until all clarifying questions have been answered.  
- Always use the provided PRD skeleton template for consistency.
