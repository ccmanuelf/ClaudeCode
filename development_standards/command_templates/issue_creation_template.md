# Issue Creation Template

## Overview
This template provides a structured approach for creating comprehensive GitHub issues within the ClaudeCode project. It ensures consistent issue documentation, proper categorization, and effective tracking throughout the development lifecycle.

## Template Structure

### **Issue Header**
```
Title: [Type]: Brief descriptive title
Labels: type-{bug|feature|enhancement|task}, priority-{critical|high|medium|low}, phase-{1|2|3|4|5}
Assignee: {github_username}
Milestone: {milestone_name}
Project: ClaudeCode Development
```

### **Issue Classification**
```
## Issue Classification

**Type:** {bug|feature|enhancement|documentation|refactor|performance|security|task}
**Priority:** {critical|high|medium|low}
**Complexity:** {simple|moderate|complex|epic}
**Phase:** {P1.1|P1.2|P1.3|P2.1|P2.2|P2.3|P3.1|P3.2|P3.3|P4.1|P4.2|P4.3|P5.1|P5.2|P5.3}
**Component:** {config-validation|progress-tracking|workflow-engine|template-system|checkpoint-recovery}
**Estimated Effort:** {1-2 hours|half day|1 day|2-3 days|1 week|2+ weeks}
```

### **Problem Description**
```
## Problem Description

**Summary:**
{Brief one-sentence description of the issue}

**Background:**
{Context and background information explaining why this issue exists}

**Current Behavior:**
{Detailed description of the current state or behavior}

**Expected Behavior:**
{Clear description of what should happen instead}

**Impact:**
{Who is affected and how this impacts the project or users}
```

### **Detailed Requirements**
```
## Detailed Requirements

### Functional Requirements
- [ ] Requirement 1: {detailed_functional_requirement_1}
- [ ] Requirement 2: {detailed_functional_requirement_2}
- [ ] Requirement 3: {detailed_functional_requirement_3}

### Non-Functional Requirements
- [ ] Performance: {performance_requirement}
- [ ] Security: {security_requirement}
- [ ] Usability: {usability_requirement}
- [ ] Reliability: {reliability_requirement}

### Constraints
- {constraint_1}
- {constraint_2}
- {constraint_3}
```

### **Acceptance Criteria**
```
## Acceptance Criteria

### Definition of Done
- [ ] Feature implemented according to specifications
- [ ] Unit tests written with >= 90% coverage
- [ ] Integration tests passing
- [ ] Documentation updated (user and technical)
- [ ] Code reviewed and approved
- [ ] Performance benchmarks met
- [ ] Security review completed (if applicable)
- [ ] Accessibility requirements met (if applicable)

### User Acceptance Criteria
- [ ] Acceptance Criterion 1: {specific_testable_criterion_1}
- [ ] Acceptance Criterion 2: {specific_testable_criterion_2}
- [ ] Acceptance Criterion 3: {specific_testable_criterion_3}

### Technical Acceptance Criteria
- [ ] Technical Criterion 1: {technical_requirement_1}
- [ ] Technical Criterion 2: {technical_requirement_2}
- [ ] Technical Criterion 3: {technical_requirement_3}
```

### **Steps to Reproduce** (For Bugs)
```
## Steps to Reproduce

**Environment:**
- OS: {operating_system}
- Python Version: {python_version}
- ClaudeCode Version: {claudecode_version}
- Browser (if applicable): {browser_version}

**Reproduction Steps:**
1. {step_1}
2. {step_2}
3. {step_3}
4. {step_4}

**Expected Result:**
{what_should_happen}

**Actual Result:**
{what_actually_happens}

**Frequency:**
{always|sometimes|rarely} - {percentage_if_known}%

**Workaround:**
{temporary_workaround_if_available}
```

### **Proposed Solution** (For Features/Enhancements)
```
## Proposed Solution

### High-Level Approach
{overview_of_proposed_solution}

### Technical Implementation
1. **Component Changes:**
   - {component_1}: {changes_needed}
   - {component_2}: {changes_needed}
   - {component_3}: {changes_needed}

2. **New Components:**
   - {new_component_1}: {purpose_and_functionality}
   - {new_component_2}: {purpose_and_functionality}

3. **Data Model Changes:**
   - {data_change_1}
   - {data_change_2}

4. **API Changes:**
   - {api_change_1}
   - {api_change_2}

### Alternative Solutions Considered
1. **Alternative 1:** {alternative_description}
   - Pros: {pros}
   - Cons: {cons}
   - Reason not chosen: {reason}

2. **Alternative 2:** {alternative_description}
   - Pros: {pros}
   - Cons: {cons}
   - Reason not chosen: {reason}
```

### **Technical Details**
```
## Technical Details

### Architecture Impact
- **Affected Components:** {list_of_components}
- **New Dependencies:** {new_dependencies}
- **Breaking Changes:** {yes|no} - {details_if_yes}
- **Migration Required:** {yes|no} - {migration_plan_if_yes}

### Implementation Notes
- {implementation_note_1}
- {implementation_note_2}
- {implementation_note_3}

### Configuration Changes
```yaml
# Configuration changes required
{configuration_section}:
  {new_setting}: {value}
  {modified_setting}: {new_value}
```

### Database Changes
- {database_change_1}
- {database_change_2}
- {database_change_3}
```

### **Dependencies and Relationships**
```
## Dependencies and Relationships

### Prerequisites
- [ ] Issue #{issue_number}: {prerequisite_issue_title}
- [ ] Issue #{issue_number}: {prerequisite_issue_title}
- [ ] Issue #{issue_number}: {prerequisite_issue_title}

### Blocking Issues
- [ ] Issue #{issue_number}: {blocking_issue_title}
- [ ] Issue #{issue_number}: {blocking_issue_title}

### Related Issues
- Issue #{issue_number}: {related_issue_title}
- Issue #{issue_number}: {related_issue_title}

### Child Issues (For Epics)
- [ ] Issue #{issue_number}: {child_issue_title}
- [ ] Issue #{issue_number}: {child_issue_title}
- [ ] Issue #{issue_number}: {child_issue_title}
```

### **Testing Strategy**
```
## Testing Strategy

### Test Categories
- **Unit Tests:** {unit_test_description}
  - Coverage Target: {coverage_percentage}%
  - Framework: {testing_framework}

- **Integration Tests:** {integration_test_description}
  - Components to test: {components_list}
  - Test scenarios: {scenario_count}

- **System Tests:** {system_test_description}
  - End-to-end workflows: {workflow_list}
  - Performance tests: {performance_test_description}

- **User Acceptance Tests:** {uat_description}
  - Test users: {test_user_roles}
  - Test scenarios: {uat_scenario_count}

### Test Data Requirements
- {test_data_requirement_1}
- {test_data_requirement_2}
- {test_data_requirement_3}

### Performance Testing
- **Load Testing:** {load_test_requirements}
- **Stress Testing:** {stress_test_requirements}
- **Performance Benchmarks:** {benchmark_requirements}
```

### **Documentation Requirements**
```
## Documentation Requirements

### User Documentation
- [ ] User guide updates: {user_guide_sections}
- [ ] API documentation: {api_doc_changes}
- [ ] Configuration guide: {config_doc_changes}
- [ ] Troubleshooting guide: {troubleshooting_additions}

### Technical Documentation
- [ ] Architecture documentation: {architecture_doc_changes}
- [ ] Code documentation: {code_doc_requirements}
- [ ] Deployment guide: {deployment_doc_changes}
- [ ] Monitoring guide: {monitoring_doc_changes}

### Examples and Tutorials
- [ ] Code examples: {example_requirements}
- [ ] Tutorial updates: {tutorial_changes}
- [ ] Best practices: {best_practice_additions}
```

### **Risk Assessment**
```
## Risk Assessment

### Technical Risks
1. **Risk:** {technical_risk_1}
   - **Probability:** {high|medium|low}
   - **Impact:** {high|medium|low}
   - **Mitigation:** {mitigation_strategy}

2. **Risk:** {technical_risk_2}
   - **Probability:** {high|medium|low}
   - **Impact:** {high|medium|low}
   - **Mitigation:** {mitigation_strategy}

### Business Risks
1. **Risk:** {business_risk_1}
   - **Probability:** {high|medium|low}
   - **Impact:** {high|medium|low}
   - **Mitigation:** {mitigation_strategy}

### Security Considerations
- {security_consideration_1}
- {security_consideration_2}
- {security_consideration_3}

### Performance Considerations
- {performance_consideration_1}
- {performance_consideration_2}
- {performance_consideration_3}
```

### **Implementation Plan**
```
## Implementation Plan

### Phase 1: Planning and Design
- [ ] Task 1: {planning_task_1} - {effort_estimate}
- [ ] Task 2: {planning_task_2} - {effort_estimate}
- [ ] Task 3: {planning_task_3} - {effort_estimate}
- **Duration:** {phase_1_duration}

### Phase 2: Core Implementation
- [ ] Task 1: {implementation_task_1} - {effort_estimate}
- [ ] Task 2: {implementation_task_2} - {effort_estimate}
- [ ] Task 3: {implementation_task_3} - {effort_estimate}
- **Duration:** {phase_2_duration}

### Phase 3: Testing and Integration
- [ ] Task 1: {testing_task_1} - {effort_estimate}
- [ ] Task 2: {testing_task_2} - {effort_estimate}
- [ ] Task 3: {testing_task_3} - {effort_estimate}
- **Duration:** {phase_3_duration}

### Phase 4: Documentation and Deployment
- [ ] Task 1: {documentation_task_1} - {effort_estimate}
- [ ] Task 2: {deployment_task_1} - {effort_estimate}
- [ ] Task 3: {finalization_task_1} - {effort_estimate}
- **Duration:** {phase_4_duration}

### Total Timeline
- **Estimated Start:** {start_date}
- **Estimated Completion:** {completion_date}
- **Total Effort:** {total_effort}
```

### **Resources and Assets**
```
## Resources and Assets

### Code Repositories
- Main Repository: {main_repo_url}
- Related Repositories: {related_repo_urls}

### Documentation Links
- Specification: {spec_link}
- Design Documents: {design_doc_links}
- API Documentation: {api_doc_link}

### External References
- {external_reference_1}
- {external_reference_2}
- {external_reference_3}

### Attachments
- Screenshots: {screenshot_links}
- Mockups: {mockup_links}
- Diagrams: {diagram_links}
- Test Data: {test_data_links}
```

### **Communication Plan**
```
## Communication Plan

### Stakeholders
- **Primary:** {primary_stakeholder}
- **Secondary:** {secondary_stakeholders}
- **Reviewers:** {technical_reviewers}
- **Approvers:** {final_approvers}

### Status Updates
- **Frequency:** {update_frequency}
- **Format:** {update_format}
- **Channel:** {communication_channel}

### Decision Points
- Decision 1: {decision_description} - Date: {decision_date}
- Decision 2: {decision_description} - Date: {decision_date}

### Review Schedule
- Design Review: {design_review_date}
- Code Review: {code_review_date}
- Testing Review: {testing_review_date}
- Final Review: {final_review_date}
```

## Issue Types and Templates

### **Bug Report Template**
```
**Bug Summary:** {one_line_summary}
**Severity:** {critical|high|medium|low}
**Priority:** {p1|p2|p3|p4}
**Component:** {affected_component}
**Version:** {version_number}

**Environment Details:**
- OS: {operating_system}
- Browser: {browser_if_applicable}
- Configuration: {relevant_config}

**Steps to Reproduce:**
1. {step_1}
2. {step_2}
3. {step_3}

**Expected vs Actual:**
- Expected: {expected_behavior}
- Actual: {actual_behavior}

**Additional Context:**
{screenshots_logs_additional_info}
```

### **Feature Request Template**
```
**Feature Summary:** {one_line_summary}
**User Story:** As a {user_type}, I want {functionality} so that {benefit}
**Priority:** {high|medium|low}
**Complexity:** {simple|moderate|complex}

**Problem Statement:**
{problem_description}

**Proposed Solution:**
{solution_description}

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Success Metrics:**
{how_to_measure_success}
```

### **Task Template**
```
**Task Summary:** {one_line_summary}
**Category:** {development|testing|documentation|infrastructure|research}
**Priority:** {high|medium|low}
**Effort:** {effort_estimate}

**Description:**
{detailed_task_description}

**Deliverables:**
- [ ] Deliverable 1
- [ ] Deliverable 2
- [ ] Deliverable 3

**Definition of Done:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

## Best Practices

### **Issue Creation**
1. **Clear Titles**: Use descriptive, action-oriented titles
2. **Proper Labels**: Apply consistent labeling for easy filtering
3. **Complete Information**: Fill out all relevant sections
4. **Link Related Issues**: Connect dependencies and relationships

### **Writing Guidelines**
1. **Be Specific**: Avoid vague descriptions
2. **Use Examples**: Provide concrete examples where helpful
3. **Include Context**: Explain the "why" behind requests
4. **Keep Updated**: Maintain current information throughout lifecycle

### **Collaboration**
1. **Tag Stakeholders**: Mention relevant team members
2. **Regular Updates**: Provide progress updates
3. **Document Decisions**: Record important decisions in comments
4. **Close Properly**: Ensure proper closure with summary

---

**Note**: This template should be customized based on the specific issue type and context. Remove sections that don't apply and add issue-specific details as needed.