# Do Task Template

## Overview
This template provides a structured approach for executing tasks within the ClaudeCode development workflow. It ensures consistent task execution, proper documentation, and effective progress tracking.

## Template Structure

### **Task Identification**
```
Task ID: {task_id}
Task Name: {task_name}
Phase: {phase}
Priority: {priority}
Estimated Effort: {estimated_effort}
Dependencies: {dependencies}
```

### **Task Context**
```
## Context
**Background:** {background_information}
**Problem Statement:** {problem_description}
**Success Criteria:** {success_criteria}
**Constraints:** {constraints}
```

### **Pre-Task Checklist**
- [ ] Dependencies verified and completed
- [ ] Required resources available
- [ ] Environment properly configured
- [ ] Backup/checkpoint created if needed
- [ ] Task requirements clearly understood

### **Execution Plan**
```
## Step-by-Step Execution Plan

### Phase 1: Preparation
1. {preparation_step_1}
2. {preparation_step_2}
3. {preparation_step_3}

### Phase 2: Implementation
1. {implementation_step_1}
2. {implementation_step_2}  
3. {implementation_step_3}

### Phase 3: Validation
1. {validation_step_1}
2. {validation_step_2}
3. {validation_step_3}

### Phase 4: Documentation
1. {documentation_step_1}
2. {documentation_step_2}
3. {documentation_step_3}
```

### **Progress Tracking**
```
## Progress Tracking

**Start Time:** {start_timestamp}
**Current Status:** {current_status}
**Completion Percentage:** {completion_percentage}%

### Milestones
- [ ] Milestone 1: {milestone_1} - {milestone_1_date}
- [ ] Milestone 2: {milestone_2} - {milestone_2_date}
- [ ] Milestone 3: {milestone_3} - {milestone_3_date}

### Blockers/Issues
- {blocker_1} - Status: {blocker_1_status}
- {blocker_2} - Status: {blocker_2_status}
```

### **Quality Assurance**
```
## Quality Checks

### Code Quality
- [ ] Code follows project standards
- [ ] Functions properly documented
- [ ] Error handling implemented
- [ ] Performance considerations addressed

### Testing
- [ ] Unit tests written and passing
- [ ] Integration tests completed
- [ ] Edge cases tested
- [ ] Performance tests passed

### Documentation
- [ ] User documentation updated
- [ ] Technical documentation complete
- [ ] Code comments adequate
- [ ] Examples provided where needed
```

### **Deliverables**
```
## Deliverables

### Primary Deliverables
1. {deliverable_1}
   - Description: {deliverable_1_description}
   - Location: {deliverable_1_location}
   - Status: {deliverable_1_status}

2. {deliverable_2}
   - Description: {deliverable_2_description}
   - Location: {deliverable_2_location}
   - Status: {deliverable_2_status}

### Supporting Deliverables
1. {supporting_deliverable_1}
2. {supporting_deliverable_2}
3. {supporting_deliverable_3}
```

### **Testing and Validation**
```
## Testing Strategy

### Test Categories
- **Unit Tests:** {unit_test_description}
- **Integration Tests:** {integration_test_description}
- **System Tests:** {system_test_description}
- **Performance Tests:** {performance_test_description}

### Test Execution
```bash
# Run unit tests
python -m pytest tests/unit/ -v

# Run integration tests
python -m pytest tests/integration/ -v

# Run performance tests
python -m pytest tests/performance/ -v --benchmark-only
```

### Validation Criteria
- [ ] All tests pass
- [ ] Code coverage >= 90%
- [ ] Performance benchmarks met
- [ ] Integration points validated
- [ ] Error scenarios handled
```

### **Deployment/Integration**
```
## Deployment Steps

### Pre-Deployment
1. {pre_deployment_step_1}
2. {pre_deployment_step_2}
3. {pre_deployment_step_3}

### Deployment
1. {deployment_step_1}
2. {deployment_step_2}
3. {deployment_step_3}

### Post-Deployment
1. {post_deployment_step_1}
2. {post_deployment_step_2}
3. {post_deployment_step_3}

### Rollback Plan
1. {rollback_step_1}
2. {rollback_step_2}
3. {rollback_step_3}
```

### **Communication and Handoff**
```
## Communication Plan

### Status Updates
- **Frequency:** {update_frequency}
- **Recipients:** {status_recipients}
- **Format:** {status_format}

### Handoff Documentation
- **Knowledge Transfer:** {knowledge_transfer_plan}
- **Training Required:** {training_requirements}
- **Support Transition:** {support_transition_plan}
```

### **Post-Task Review**
```
## Post-Task Review

### Completion Summary
**Completion Date:** {completion_date}
**Final Status:** {final_status}
**Actual Effort:** {actual_effort}

### Success Metrics
- {success_metric_1}: {metric_1_result}
- {success_metric_2}: {metric_2_result}
- {success_metric_3}: {metric_3_result}

### Lessons Learned
#### What Went Well
1. {success_factor_1}
2. {success_factor_2}
3. {success_factor_3}

#### Challenges Encountered
1. {challenge_1}
   - Impact: {challenge_1_impact}
   - Resolution: {challenge_1_resolution}

2. {challenge_2}
   - Impact: {challenge_2_impact}
   - Resolution: {challenge_2_resolution}

#### Recommendations for Future Tasks
1. {recommendation_1}
2. {recommendation_2}
3. {recommendation_3}
```

### **Files and Resources**
```
## Related Files
- Configuration: {config_files}
- Documentation: {documentation_files}
- Tests: {test_files}
- Scripts: {script_files}

## External Resources
- References: {external_references}
- Dependencies: {external_dependencies}
- Tools Used: {tools_used}
```

## Usage Instructions

### **1. Task Initiation**
```bash
# Create new task from template
cp templates/do_task_template.md tasks/task_{task_id}_{task_name}.md

# Fill in task-specific information
# Update progress tracking regularly
# Create checkpoints at key milestones
```

### **2. Progress Management**
```bash
# Update progress state
python scripts/resume_progress.py update_task {task_id} {completion_percentage}

# Create checkpoint
python scripts/resume_progress.py checkpoint "Task {task_id} - {milestone_description}"

# Track blockers
python scripts/resume_progress.py analyze_blocker "{blocker_description}"
```

### **3. Quality Gates**
```bash
# Run quality checks
python scripts/quality_check.py --task {task_id}

# Validate deliverables
python scripts/validate_deliverables.py --task {task_id}

# Generate completion report
python scripts/task_report.py --task {task_id}
```

## Best Practices

### **Task Execution**
1. **Break Down Complex Tasks**: Divide large tasks into smaller, manageable subtasks
2. **Regular Updates**: Update progress and documentation frequently
3. **Quality First**: Don't compromise on quality for speed
4. **Test Early**: Implement testing throughout development, not just at the end

### **Documentation**
1. **Real-Time Updates**: Update documentation as you work, not after completion
2. **Clear Communication**: Write for future developers who will maintain the code
3. **Examples**: Include practical examples in documentation
4. **Version Control**: Track all changes and decisions

### **Collaboration**
1. **Transparent Communication**: Keep stakeholders informed of progress and blockers
2. **Knowledge Sharing**: Document decisions and rationale for future reference
3. **Peer Review**: Have work reviewed by team members before completion
4. **Handoff Planning**: Prepare for knowledge transfer early in the process

---

**Note**: This template should be customized for each specific task. Remove sections that don't apply and add task-specific sections as needed.