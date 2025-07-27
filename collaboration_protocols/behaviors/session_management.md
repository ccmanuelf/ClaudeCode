---
id: session_management
category: behavior
priority: 35
version: 1.0
description: >
  Manages AI development session lifecycle, context persistence,
  progress tracking, and knowledge capture across development
  interactions and workflow transitions.
---

## Purpose

Establish comprehensive session management capabilities that maintain context continuity, track development progress, capture decisions and learnings, and provide seamless transitions between development activities and sessions.

## Core Session Management Philosophy

> "Every session should build upon previous work while maintaining clear boundaries and context"

Session management ensures that development work maintains continuity across interactions while preserving the ability to start fresh when needed, creating a balance between persistence and flexibility.

## Session Lifecycle Management

### Session Initialization

#### Context Loading
```markdown
1. **Previous Session Recovery**
   - Load relevant context from previous sessions
   - Identify incomplete tasks and open questions
   - Restore active file context and project state
   - Validate context currency and relevance

2. **Goal Setting**
   - Clarify primary objectives for current session
   - Establish success criteria and completion markers
   - Identify dependencies and constraints
   - Set time boundaries and scope limits

3. **Environment Preparation**
   - Validate development environment status
   - Confirm tool availability and functionality
   - Load necessary project context and documentation
   - Initialize progress tracking mechanisms
```

#### Session Configuration
```json
{
  "session_config": {
    "session_id": "[unique_identifier]",
    "start_time": "[timestamp]",
    "primary_objective": "[main_goal]",
    "context_depth": "[lite|standard|comprehensive]",
    "active_workflows": ["[workflow_names]"],
    "loaded_context": ["[context_areas]"],
    "progress_tracking": true,
    "auto_documentation": true
  }
}
```

### Active Session Management

#### Progress Tracking
```markdown
1. **Task Progress Monitoring**
   - Track completion of individual tasks and subtasks
   - Monitor progress against session objectives
   - Identify bottlenecks and blockers
   - Update progress indicators regularly

2. **Decision Documentation**
   - Record key decisions made during session
   - Capture rationale and alternatives considered
   - Note stakeholders involved in decisions
   - Link decisions to relevant project context

3. **Knowledge Capture**
   - Document new learnings and insights
   - Record successful patterns and approaches
   - Note failed attempts and lessons learned
   - Capture useful resources and references
```

#### Context Maintenance
```markdown
1. **Dynamic Context Updates**
   - Refresh context as project state changes
   - Add new information as it becomes relevant
   - Remove outdated or irrelevant context
   - Maintain context coherence and accuracy

2. **State Synchronization**
   - Keep session state aligned with project reality
   - Update task lists and progress indicators
   - Sync with external systems (GitHub, project boards)
   - Validate consistency across information sources

3. **Attention Management**
   - Focus on most relevant information for current task
   - Filter noise and distracting information
   - Maintain awareness of broader project context
   - Balance detail with big-picture understanding
```

### Session Conclusion

#### Progress Summarization
```markdown
1. **Accomplishment Summary**
   - List completed tasks and achievements
   - Highlight key decisions and outcomes
   - Note progress toward session objectives
   - Identify any scope changes or discoveries

2. **Outstanding Items**
   - Document incomplete tasks and reasons
   - Identify blockers and dependency issues
   - Note questions requiring future attention
   - List follow-up actions needed

3. **Next Steps Planning**
   - Suggest logical continuation points
   - Identify priority items for next session
   - Note any urgency or time-sensitive items
   - Recommend resource allocation
```

#### Knowledge Persistence
```markdown
1. **Session Documentation**
   - Create comprehensive session summary
   - Document key learnings and insights
   - Record important decisions and rationale
   - Note any process improvements identified

2. **Context Preservation**
   - Save relevant context for future sessions
   - Update project knowledge base
   - Preserve working state and progress
   - Clean up temporary or outdated information

3. **Handoff Preparation**
   - Prepare clear handoff documentation
   - Ensure continuity for next session
   - Validate information completeness
   - Test context restoration capabilities
```

## Session State Management

### State Persistence
```json
{
  "session_state": {
    "current_phase": "[planning|implementation|review|testing]",
    "active_tasks": [
      {
        "task_id": "[identifier]",
        "description": "[task_description]",
        "status": "[not_started|in_progress|blocked|completed]",
        "progress": "[percentage_complete]",
        "blockers": ["[blocking_issues]"],
        "next_actions": ["[required_steps]"]
      }
    ],
    "decisions_made": [
      {
        "decision": "[what_was_decided]",
        "rationale": "[why_this_choice]",
        "alternatives": ["[options_considered]"],
        "timestamp": "[when_decided]"
      }
    ],
    "context_stack": [
      {
        "context_type": "[global|project|task|session]",
        "content": "[context_information]",
        "relevance": "[high|medium|low]",
        "last_updated": "[timestamp]"
      }
    ]
  }
}
```

### State Transitions
```markdown
1. **Phase Transitions**
   - Planning → Implementation: Validate specifications and setup
   - Implementation → Review: Ensure completeness and quality
   - Review → Testing: Confirm functionality and requirements
   - Testing → Deployment: Validate production readiness

2. **Context Switching**
   - Task switching: Preserve current state, load new context
   - Project switching: Save project state, load different project
   - Mode switching: Adjust verbosity and detail levels
   - Priority switching: Reorder tasks based on new priorities

3. **State Recovery**
   - Session restoration: Reload previous session state
   - Error recovery: Restore stable state after failures
   - Context recovery: Rebuild context from persistent storage
   - Progress recovery: Restore task progress and decisions
```

## Integration Patterns

### Workflow Integration
```markdown
1. **Workflow State Tracking**
   - Monitor progress through workflow stages
   - Track completion of workflow milestones
   - Identify workflow bottlenecks and issues
   - Coordinate between multiple active workflows

2. **Cross-Workflow Communication**
   - Share context between related workflows
   - Coordinate dependencies across workflows
   - Manage resource conflicts and priorities
   - Ensure consistency in cross-workflow decisions

3. **Workflow Handoffs**
   - Smooth transitions between workflow phases
   - Clear documentation of handoff points
   - Validation of handoff completeness
   - Accountability for handoff quality
```

### Tool Integration
```markdown
1. **Development Tool State**
   - Track state of development tools and environments
   - Monitor tool availability and functionality
   - Coordinate tool usage across tasks
   - Handle tool failures and recovery

2. **External System Sync**
   - Synchronize with GitHub issues and PRs
   - Update project management systems
   - Coordinate with CI/CD pipelines
   - Maintain documentation systems

3. **Communication Platforms**
   - Update team communication channels
   - Share progress with stakeholders
   - Coordinate with team members
   - Manage notification and alert systems
```

## Session Templates

### Session Initialization Template
```markdown
# Session Start: [DATE] - [PRIMARY_OBJECTIVE]

## Context Loading
- Previous session: [REFERENCE_OR_NONE]
- Project state: [CURRENT_PHASE]
- Active context: [LOADED_AREAS]
- Available time: [TIME_ALLOCATION]

## Session Goals
- Primary objective: [MAIN_GOAL]
- Success criteria: [HOW_TO_MEASURE_SUCCESS]
- Scope boundaries: [WHAT_IS_IN_OUT_OF_SCOPE]
- Dependencies: [WHAT_IS_NEEDED]

## Starting State
- Active tasks: [CURRENT_TASKS]
- Known blockers: [EXISTING_ISSUES]
- Available resources: [TOOLS_PEOPLE_TIME]
- Priority constraints: [URGENCY_FACTORS]
```

### Session Summary Template
```markdown
# Session Summary: [DATE] - [DURATION]

## Accomplishments
- Completed tasks: [LIST_OF_COMPLETED_WORK]
- Key decisions: [IMPORTANT_CHOICES_MADE]
- Progress made: [ADVANCEMENT_SUMMARY]
- Learnings: [NEW_INSIGHTS_GAINED]

## Outstanding Items
- Incomplete tasks: [UNFINISHED_WORK]
- Identified blockers: [ISSUES_DISCOVERED]
- Open questions: [UNRESOLVED_ITEMS]
- Follow-up needed: [NEXT_ACTIONS_REQUIRED]

## Next Session Preparation
- Recommended focus: [SUGGESTED_PRIORITIES]
- Context to preserve: [IMPORTANT_STATE]
- Resources needed: [TOOLS_PEOPLE_INFO]
- Estimated timeline: [TIME_EXPECTATIONS]

## Process Notes
- What worked well: [SUCCESSFUL_APPROACHES]
- What could improve: [OPTIMIZATION_OPPORTUNITIES]
- Tools/methods used: [TECHNIQUES_APPLIED]
- Efficiency observations: [PRODUCTIVITY_INSIGHTS]
```

## Quality Assurance

### Session Quality Metrics
```json
{
  "quality_metrics": {
    "objective_completion": "[percentage_of_goals_achieved]",
    "context_accuracy": "[quality_of_maintained_context]",
    "decision_quality": "[soundness_of_choices_made]",
    "progress_efficiency": "[advancement_per_time_unit]",
    "knowledge_capture": "[completeness_of_documentation]"
  }
}
```

### Session Validation Checklist
- [ ] Clear objectives established at session start
- [ ] Relevant context loaded and validated
- [ ] Progress tracked throughout session
- [ ] Key decisions documented with rationale
- [ ] Outstanding items clearly identified
- [ ] Next steps planned and prioritized
- [ ] Session summary complete and accurate
- [ ] Context properly preserved for future use

## Best Practices

### Session Planning
1. **Clear Objectives:** Start each session with specific, measurable goals
2. **Realistic Scope:** Set achievable objectives within available time
3. **Context Preparation:** Load relevant information before beginning work
4. **Resource Validation:** Confirm tool and information availability
5. **Flexibility Planning:** Allow for unexpected discoveries or changes

### Session Execution
1. **Regular Check-ins:** Monitor progress against objectives periodically
2. **Decision Documentation:** Record important choices as they're made
3. **Context Maintenance:** Keep information current and relevant
4. **Blocker Management:** Address obstacles promptly and document resolutions
5. **Quality Focus:** Maintain standards while making progress

### Session Conclusion
1. **Comprehensive Summary:** Document all significant work and decisions
2. **Honest Assessment:** Evaluate both successes and shortcomings
3. **Knowledge Capture:** Record learnings and insights for future benefit
4. **Clean Handoff:** Prepare clear information for session continuation
5. **Process Reflection:** Consider improvements for future sessions

## Common Patterns

### Successful Session Patterns
- **Focused Start:** Clear objective setting and context loading
- **Steady Progress:** Regular advancement with periodic validation
- **Quality Gates:** Checkpoints ensuring work meets standards
- **Clean Completion:** Proper documentation and handoff preparation

### Problem Recovery Patterns
- **Context Loss:** Systematic reconstruction from available information
- **Progress Stalling:** Root cause analysis and approach adjustment
- **Scope Creep:** Objective refocusing and priority clarification
- **Quality Issues:** Validation processes and remediation strategies

## Integration Commands

### Session Management Commands
```json
{
  "session_commands": {
    "/session_start [objective]": "Initialize new development session",
    "/session_status": "Show current session progress and state",
    "/session_checkpoint": "Save current progress and context",
    "/session_summary": "Generate comprehensive session summary",
    "/session_handoff": "Prepare session for continuation or transfer",
    "/session_recover [session_id]": "Restore previous session state"
  }
}
```

### Context Management Commands
```json
{
  "context_commands": {
    "/context_save": "Preserve current context state",
    "/context_load [context_id]": "Restore saved context",
    "/context_update [area]": "Refresh specific context area",
    "/context_clean": "Remove outdated context information",
    "/context_validate": "Check context accuracy and completeness"
  }
}
```

This session management behavior ensures effective coordination of development activities across time boundaries while maintaining context continuity and progress visibility throughout the development lifecycle.