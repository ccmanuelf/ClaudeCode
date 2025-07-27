---
id: test_driven_development
category: workflow
priority: 40
version: 1.0
description: >
  Implements Test-Driven Development (TDD) methodology with detailed,
  step-by-step blueprint creation and iterative development cycles
  optimized for AI-assisted development.
---

## Purpose

Establish a comprehensive TDD workflow that emphasizes detailed planning, incremental progress, and strong testing practices. This workflow creates a series of well-sized, testable development steps that build systematically toward project completion.

## Core TDD Philosophy

> "Red, Green, Refactor" - Write failing tests, make them pass, improve the code

TDD transforms development from reactive coding to proactive design, ensuring every piece of code serves a verified purpose and meets defined requirements.

## The TDD Workflow Process

### Phase 1: Blueprint Creation

#### Step 1: Analyze and Plan
```markdown
1. Analyze the project specification thoroughly
2. Draft detailed, step-by-step blueprint for entire project
3. Break blueprint into small, iterative chunks that build on each other
4. Review chunks and break down further if needed
5. Iterate until steps are right-sized for safe implementation
```

#### Step 2: Validate Step Sizing
**Optimal Step Criteria:**
- **Small enough:** Can be implemented safely with comprehensive testing
- **Large enough:** Moves project meaningfully forward
- **Self-contained:** Each step produces working, testable functionality
- **Sequential:** Each step builds logically on previous steps
- **Integrated:** No orphaned or hanging code

#### Step 3: Create Implementation Prompts
Generate AI-ready prompts for each step:
- **Context:** Background and current state
- **Objective:** What this step accomplishes
- **Acceptance Criteria:** How to know when step is complete
- **Testing Requirements:** What tests must be written
- **Integration Notes:** How step connects to previous work

### Phase 2: TDD Implementation Cycle

#### Red Phase: Write Failing Tests
```markdown
1. **Understand the Requirement**
   - Review step specification
   - Identify expected behavior
   - Define success criteria

2. **Write Minimal Failing Test**
   - Test one specific behavior
   - Use descriptive test names
   - Include edge cases
   - Verify test fails for right reason

3. **Run Test Suite**
   - Confirm new test fails
   - Ensure existing tests still pass
   - Validate test failure message
```

#### Green Phase: Make Tests Pass
```markdown
1. **Write Minimal Code**
   - Implement just enough to pass the test
   - Avoid over-engineering
   - Focus on making test green

2. **Run Test Suite**
   - Confirm failing test now passes
   - Ensure no regressions in existing tests
   - Validate all tests green

3. **Commit Working State**
   - Commit passing tests and minimal implementation
   - Use descriptive commit messages
   - Maintain clean git history
```

#### Refactor Phase: Improve Design
```markdown
1. **Identify Improvement Opportunities**
   - Code duplication
   - Poor naming
   - Complex logic
   - Design patterns

2. **Refactor Incrementally**
   - Make one improvement at a time
   - Run tests after each change
   - Maintain all tests passing

3. **Validate and Commit**
   - Ensure all tests still pass
   - Commit refactoring separately
   - Document design decisions
```

### Phase 3: Integration and Validation

#### Step Integration
```markdown
1. **Wire Components Together**
   - Connect new functionality to existing system
   - Update integration points
   - Ensure end-to-end functionality

2. **Integration Testing**
   - Test component interactions
   - Validate data flow
   - Confirm system behavior

3. **System Validation**
   - Run full test suite
   - Perform manual validation
   - Check performance impact
```

## File Organization Structure

### Planning Files
```
plan.md              # Detailed project blueprint
todo.md             # Current state and task tracking
prompts/            # Generated AI implementation prompts
├── step-01-prompt.md
├── step-02-prompt.md
└── step-n-prompt.md
```

### Implementation Files
```
tests/              # Test files organized by feature
├── unit/
├── integration/
└── e2e/
src/                # Source code organized by component
docs/               # Documentation and design decisions
```

## TDD Best Practices

### Test Design Principles
1. **Arrange, Act, Assert:** Structure tests clearly
2. **One Assertion Per Test:** Focus on single behavior
3. **Descriptive Names:** Test names should tell a story
4. **Independent Tests:** No dependencies between tests
5. **Fast Execution:** Tests should run quickly

### Code Development Guidelines
1. **Minimal Implementation:** Write least code to pass tests
2. **Single Responsibility:** Each function/class has one purpose
3. **Clear Interfaces:** Well-defined inputs and outputs
4. **Error Handling:** Test and implement error scenarios
5. **Documentation:** Code should be self-documenting

### Refactoring Standards
1. **Preserve Behavior:** Never change functionality during refactoring
2. **Incremental Changes:** Small, focused improvements
3. **Test Coverage:** Maintain or improve test coverage
4. **Design Patterns:** Apply appropriate patterns consistently
5. **Performance Awareness:** Monitor impact on system performance

## Quality Gates

### Step Completion Criteria
- [ ] All planned tests written and passing
- [ ] Code coverage meets project standards
- [ ] Integration with previous steps verified
- [ ] Documentation updated
- [ ] No code quality violations

### Phase Completion Criteria
- [ ] All steps in phase completed
- [ ] Full test suite passing
- [ ] Integration tests verified
- [ ] Performance benchmarks met
- [ ] Code review completed

### Project Completion Criteria
- [ ] All requirements implemented
- [ ] Comprehensive test coverage achieved
- [ ] Documentation complete and current
- [ ] Performance requirements met
- [ ] Security requirements addressed

## Common TDD Patterns

### Test Patterns
```python
# Example: Testing a user service
def test_create_user_with_valid_data():
    # Arrange
    user_data = {"name": "John", "email": "john@example.com"}
    
    # Act
    result = user_service.create_user(user_data)
    
    # Assert
    assert result.success == True
    assert result.user.name == "John"
```

### Implementation Patterns
```python
# Example: Minimal implementation
def create_user(user_data):
    # Minimal code to pass the test
    user = User(name=user_data["name"], email=user_data["email"])
    return CreateUserResult(success=True, user=user)
```

### Refactoring Patterns
```python
# Example: Extract method refactoring
def create_user(user_data):
    validated_data = validate_user_data(user_data)
    user = build_user_from_data(validated_data)
    return save_user_to_database(user)
```

## AI Integration Guidelines

### Prompt Engineering for TDD
```markdown
## TDD Step Prompt Template
**Context:** [Current project state and completed steps]
**Objective:** [What this step accomplishes]
**TDD Phase:** [Red/Green/Refactor]

### Requirements
- [Specific functionality to implement]
- [Testing requirements]
- [Integration points]

### Acceptance Criteria
- [ ] [Specific criteria for completion]
- [ ] [Test coverage requirements]
- [ ] [Integration validation]

### Implementation Notes
- [Patterns to follow]
- [Libraries to use]
- [Constraints to respect]
```

### AI Workflow Commands
```json
{
  "tdd_commands": {
    "/tdd_start [project]": "Initialize TDD workflow for project",
    "/tdd_plan": "Create detailed implementation blueprint",
    "/tdd_step [n]": "Execute specific TDD step",
    "/tdd_test": "Write tests for current step",
    "/tdd_implement": "Implement code to pass tests",
    "/tdd_refactor": "Refactor current implementation",
    "/tdd_integrate": "Integrate step with existing code",
    "/tdd_validate": "Validate step completion",
    "/tdd_status": "Show current TDD progress"
  }
}
```

## Troubleshooting

### Common Issues
- **Tests Too Large:** Break into smaller, focused tests
- **Implementation Too Complex:** Reduce to minimal passing code
- **Integration Failures:** Review step dependencies and interfaces
- **Refactoring Breaks Tests:** Make smaller, incremental changes

### Resolution Strategies
- **Review Step Size:** Ensure steps are appropriately scoped
- **Validate Test Design:** Confirm tests focus on single behaviors
- **Check Integration Points:** Verify component interfaces
- **Analyze Failure Patterns:** Learn from recurring issues

## Success Metrics

### Process Metrics
- **Test Coverage:** Percentage of code covered by tests
- **Test Pass Rate:** Percentage of tests passing consistently
- **Refactoring Frequency:** How often code is improved
- **Integration Success:** Rate of successful step integration

### Quality Metrics
- **Defect Rate:** Number of bugs found in production
- **Code Quality Score:** Static analysis results
- **Maintainability Index:** How easy code is to modify
- **Performance Benchmarks:** System performance measurements

This TDD workflow ensures systematic, test-driven development with clear processes for planning, implementation, and validation, optimized for AI-assisted development environments.