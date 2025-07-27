---
id: development_standards
category: guardrail
priority: 90
version: 1.0
description: >
  Establishes comprehensive development standards, coding practices, testing
  requirements, and quality control measures for AI-assisted development.
---

## Core Development Principles

### Code Quality Standards
- **Simplicity First:** Prefer simple, clean, maintainable solutions over clever or complex ones
- **Readability Priority:** Code readability and maintainability are primary concerns
- **Minimal Changes:** Make the smallest reasonable changes to achieve desired outcomes
- **Style Consistency:** Match existing code style and formatting within files
- **Permission Required:** Must ask before reimplementing features or systems from scratch

### Change Management Protocol
- **Scope Discipline:** NEVER make code changes unrelated to current task
- **Issue Documentation:** Document unrelated issues for future addressing
- **Comment Preservation:** NEVER remove code comments unless actively false
- **Temporal Avoidance:** Comments should be evergreen, not about recent changes
- **File Headers:** All code files start with 2-line "ABOUTME:" comment explaining purpose

## Testing Requirements

### Mandatory Testing Policy
**NO EXCEPTIONS POLICY:** Every project MUST have:
- Unit tests
- Integration tests  
- End-to-end tests

**Override Authority:** Only proceed without tests when human explicitly states:
> "I AUTHORIZE YOU TO SKIP WRITING TESTS THIS TIME"

### Test-Driven Development (TDD)
**Required Process:**
1. Write failing test that defines desired function or improvement
2. Run test to confirm it fails as expected
3. Write minimal code to make the test pass
4. Run test to confirm success
5. Refactor code while keeping tests green
6. Repeat cycle for each new feature or bugfix

### Test Quality Standards
- **Coverage Requirements:** Tests MUST cover the functionality being implemented
- **Output Monitoring:** NEVER ignore system output or test results
- **Pristine Output:** Test output must be clean to pass
- **Error Testing:** If logs should contain errors, capture and test them
- **Comprehensive Validation:** Test both success and failure scenarios

## Git and Version Control Standards

### Commit Requirements
- **Pre-commit Compliance:** ALL pre-commit hooks must pass before commit
- **No Bypass Policy:** NEVER use `--no-verify`, `--no-hooks`, or `--no-pre-commit-hook`
- **Quality First:** Fix hook failures rather than bypassing them
- **Clean History:** Commits should represent complete, working states

### Pre-Commit Failure Protocol
When pre-commit hooks fail, follow this exact sequence:
1. **Read Complete Output:** Explain what errors are occurring
2. **Identify Root Cause:** Determine which tool failed and why
3. **Explain Fix Strategy:** State what fix will be applied and rationale
4. **Apply Fix:** Implement the correction
5. **Re-run Hooks:** Verify all hooks pass
6. **Only Then Commit:** Proceed only after complete success

### Forbidden Git Practices
**NEVER USE:** `--no-verify`, `--no-hooks`, `--no-pre-commit-hook`
**PROCESS:** Before using ANY git flag:
- State the flag intended for use
- Explain why it's needed
- Confirm it's not on forbidden list
- Get explicit human permission for any bypass flags

### Pressure Response Protocol
When urgency is applied to commit/push with failing hooks:
- **Resist Bypass Temptation:** Do NOT rush to bypass quality checks
- **Communicate Status:** "Pre-commit hooks are failing, I need to fix those first"
- **Work Systematically:** Address failures methodically
- **Maintain Standards:** Quality over speed, even under pressure

## Code Implementation Standards

### Naming Conventions
- **Evergreen Names:** Never use 'improved', 'new', 'enhanced', 'old'
- **Descriptive Names:** Names should clearly indicate purpose
- **Consistent Patterns:** Follow established naming conventions in project
- **Future-Proof:** Names should remain relevant over time

### Implementation Practices
- **No Mock Mode:** NEVER implement mock modes for testing or any purpose
- **Real Data Only:** Always use real data and real APIs
- **No Throwaway Code:** NEVER discard old implementation without explicit permission
- **Permission Protocol:** MUST STOP and get explicit permission before major rewrites

### Error Handling
- **Comprehensive Coverage:** Handle all reasonable error scenarios
- **Graceful Degradation:** System should fail gracefully, not catastrophically
- **Informative Messages:** Error messages should help users understand and resolve issues
- **Logging Integration:** Errors should be properly logged for debugging

## Quality Assurance

### Code Review Standards
- **Self-Review First:** Review your own work before presenting
- **Documentation Sync:** Ensure documentation matches implementation
- **Test Coverage:** Verify tests cover new functionality
- **Integration Testing:** Confirm changes work with existing system

### Accountability Checkpoints
Before executing any development action, ask:
- "Am I bypassing a safety mechanism?"
- "Would this action violate established standards?"
- "Am I choosing convenience over quality?"

If any answer is "yes" or "maybe", explain concerns before proceeding.

### Learning-Focused Approach
When encountering tool failures:
- **Learning Opportunity:** Treat failures as chances to improve understanding
- **Research First:** Investigate specific errors before attempting fixes
- **Knowledge Sharing:** Explain what was learned about tools/codebase
- **Skill Building:** Build competence with development tools rather than avoiding them

## Technology-Specific Standards

### Python Projects
- **Package Management:** Use `uv` for Python package management
- **No Requirements.txt:** Packages stored in `pyproject.toml`
- **Script Execution:** Run scripts with `uv run <script.py>`
- **Package Addition:** Add packages with `uv add <package>`

### Workflow Integration
- **Task Completion:** Check off completed work in `todo.md` if present
- **Testing Verification:** Ensure all tests pass before marking tasks complete
- **Linting Compliance:** Ensure linting passes before task completion
- **Documentation Updates:** Update relevant documentation with changes

## Quality Gates

### Pre-Implementation Checklist
- [ ] Requirements clearly understood
- [ ] Approach planned and validated
- [ ] Tests identified and planned
- [ ] Integration points considered

### Pre-Commit Checklist
- [ ] All tests passing
- [ ] Linting rules satisfied
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] No unrelated changes included

### Task Completion Checklist
- [ ] All acceptance criteria met
- [ ] Tests written and passing
- [ ] Code quality standards met
- [ ] Documentation current
- [ ] No regressions introduced

## Violation Response

### Minor Violations
- **Immediate Correction:** Fix immediately when noticed
- **Root Cause Analysis:** Understand why violation occurred
- **Process Improvement:** Adjust approach to prevent recurrence

### Major Violations
- **Stop Work:** Halt current activity immediately
- **Assess Impact:** Determine scope of violation effects
- **Recovery Plan:** Develop strategy to remediate
- **Get Approval:** Obtain explicit permission before proceeding

These development standards ensure consistent, high-quality code delivery while maintaining professional development practices and quality assurance throughout the development lifecycle.