---
id: generate_task_list
category: workflow
priority: 30
version: 1.0
description: >
  Create a structured implementation task list in Markdown format from an existing PRD,
  supporting phased breakdown and junior developer readability.
---

## Purpose

Help the agent convert a finalized Product Requirements Document (PRD)
into a detailed, developer-friendly task list. This list supports planning, delegation,
and implementation, especially for junior engineers unfamiliar with architectural nuance.

## Process

1. **Receive PRD Reference**  
   - User provides the PRD filename or content (e.g., `prd-user-profile-editing.md`)

2. **Analyze PRD**  
   - Extract functional requirements, user stories, acceptance criteria, and constraints  
   - Identify core features and optional enhancements

3. **Phase 1: Generate Parent Tasks**  
   - Derive 5–7 high-level implementation tasks  
   - Present to user and ask:  
     > “I’ve generated the high-level tasks based on your PRD. Ready to expand them into subtasks? Respond with ‘Go’ to continue.”  

4. **Pause for Confirmation**  
   - Await user reply `"Go"` before proceeding  

5. **Phase 2: Generate Sub-Tasks**  
   - Expand each parent task with 3–6 actionable subtasks  
   - Ensure sub-tasks cover all acceptance criteria and edge cases from the PRD

6. **Identify Relevant Files**  
   - Suggest which source, API, test, and helper files will be created or modified  
   - Include descriptions and test file pairings

7. **Generate Final Output**  
   - Assemble all elements into a structured Markdown file

8. **Save Output File**  
   - Path: `/tasks/`  
   - Filename: `tasks-prd-[original-prd-name].md`  
     - Example: `tasks-prd-user-profile-editing.md`

## Output Format

The generated file must follow this format:

```markdown
## Relevant Files

- `src/components/UserProfileForm.tsx` – Main form logic and validation
- `src/components/UserProfileForm.test.tsx` – Unit tests for form component
- `api/user/update.ts` – API handler for profile changes
- `api/user/update.test.ts` – Integration tests for endpoint
- `lib/hooks/useUserData.ts` – Reusable data fetching logic
- `lib/hooks/useUserData.test.ts` – Tests for hook behavior

### Notes

- Co-locate test files with their source files when feasible
- Use `npx jest` or `pytest` to run applicable tests
- Confirm that every critical path includes test coverage before deployment

## Tasks

- [ ] 1.0 Create User Profile Editing Form
  - [ ] 1.1 Define form fields from PRD data model
  - [ ] 1.2 Implement client-side validation
  - [ ] 1.3 Ensure accessibility compliance (labels, ARIA)
  - [ ] 1.4 Wire submission to backend API

- [ ] 2.0 Implement Backend Update Endpoint
  - [ ] 2.1 Accept payload via POST `/api/user/update`
  - [ ] 2.2 Validate incoming data server-side
  - [ ] 2.3 Persist changes to database
  - [ ] 2.4 Return success/error response

- [ ] 3.0 Add Unit and Integration Tests
  - [ ] 3.1 Write component tests using `Jest` and `React Testing Library`
  - [ ] 3.2 Write API endpoint tests using `supertest`
  - [ ] 3.3 Include edge case scenarios (e.g., empty fields, invalid input)

- [ ] 4.0 Design Review and Refactoring
  - [ ] 4.1 Request feedback on UX layout
  - [ ] 4.2 Refactor state handling logic if needed

- [ ] 5.0 Update Documentation
  - [ ] 5.1 Update README with feature overview and test instructions
  - [ ] 5.2 Create CHANGELOG entry for new functionality
