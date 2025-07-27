---
id: context_management
category: behavior
priority: 30
version: 1.0
description: >
  Implements Context Engineering principles for managing and delivering
  precise, relevant context to AI systems. Ensures optimal information
  flow without overwhelming the AI or providing insufficient context.
---

## Purpose

Context Engineering is the discipline of designing, managing, and delivering the precise, relevant context an AI needs to perform specific tasks. It solves the fundamental problem of finite context windows versus vast, complex software projects.

## Core Principles

### 1. Structured Knowledge Organization
Information is organized into logical, queryable components rather than monolithic blocks:
- **Project Vision:** High-level goals and objectives
- **Architecture Documentation:** System design and patterns
- **Specific Requirements:** Task-level specifications
- **Implementation Context:** Code references and dependencies

### 2. Layered Context Delivery
AI receives context in progressive layers from general to specific:
```
Layer 1: Project Goals & Vision
Layer 2: Architectural Patterns  
Layer 3: Specific Task Requirements
Layer 4: Implementation Details
```

### 3. Just-in-Time Context Loading
Information is provided precisely when needed, tied to specific commands or prompts:
- Minimizes cognitive noise
- Maximizes signal relevance
- Prevents context window overflow

### 4. AI-Friendly Formatting
All artifacts stored in machine-readable formats:
- **Primary:** Markdown with YAML frontmatter
- **Structured Data:** JSON templates
- **Configuration:** YAML files
- **Consistent Syntax:** Standardized patterns

## Context Management Strategies

### Context Scope Classification
```json
{
  "global": "Project-wide information (vision, architecture)",
  "domain": "Feature-area specific context",
  "task": "Single task requirements and constraints",
  "session": "Current interaction state and history"
}
```

### Context Priority Matrix
| Priority | Type | When to Load | Retention |
|----------|------|--------------|-----------|
| Critical | Core specs, current task | Always | Full session |
| High | Related components, dependencies | On demand | Active task |
| Medium | Background information | If requested | Limited |
| Low | Historical context | Explicit request | Minimal |

### Dynamic Context Assembly
Context is assembled dynamically based on:
- **Command Type:** Analysis vs. implementation vs. planning
- **Task Complexity:** Simple fixes vs. architectural changes
- **User Expertise:** Beginner-friendly vs. expert-level detail
- **Project Phase:** Discovery vs. development vs. maintenance

## Implementation Patterns

### Context Loading Commands
```json
{
  "context_commands": {
    "/load_context [scope]": "Load specific context scope",
    "/context_status": "Show current context state",
    "/context_clear": "Reset context to minimal state",
    "/context_expand [area]": "Add additional context area",
    "/context_focus [task]": "Narrow context to specific task"
  }
}
```

### Context State Management
```json
{
  "context_state": {
    "loaded_scopes": ["global", "task"],
    "active_files": ["spec.md", "architecture.md"],
    "priority_items": ["acceptance_criteria", "constraints"],
    "session_memory": "key_decisions_and_patterns",
    "cache_status": "enabled"
  }
}
```

### Intelligent Context Filtering
Automatic filtering based on:
- **Relevance Score:** How closely information relates to current task
- **Recency:** When information was last updated or accessed
- **User Preference:** Historical patterns of what information user values
- **Task Type:** Different contexts for bugs vs. features vs. refactoring

## Context Templates

### Task Context Template
```markdown
# Context: [TASK_NAME]

## Core Context
- **Goal:** [Primary objective]
- **Scope:** [Boundaries and limitations]
- **Dependencies:** [Required information/components]

## Implementation Context  
- **Patterns:** [Relevant architectural patterns]
- **Constraints:** [Technical and business limitations]
- **Integration Points:** [System interfaces]

## Background Context
- **Related Features:** [Connected functionality]
- **Historical Decisions:** [Relevant past choices]
- **User Impact:** [How changes affect users]
```

### Session Context Template
```json
{
  "session_context": {
    "objective": "[Current session goal]",
    "progress": "[Completed steps]",
    "active_files": ["[List of files in scope]"],
    "decisions_made": ["[Key choices during session]"],
    "next_steps": ["[Planned actions]"],
    "context_depth": "[lite|standard|comprehensive]"
  }
}
```

## Context Quality Gates

### Context Completeness Checklist
- [ ] All required information present
- [ ] No information overload
- [ ] Appropriate detail level for task complexity
- [ ] Clear relationships between context elements
- [ ] Up-to-date and accurate information

### Context Validation Rules
1. **Relevance Test:** All context directly relates to current task
2. **Completeness Test:** No critical information missing
3. **Clarity Test:** Information is unambiguous and well-structured
4. **Efficiency Test:** Minimal cognitive load while maximizing utility

## Integration with ClaudeCode

### Automatic Context Loading
- **Project Initialization:** Load global context (vision, architecture)
- **Task Start:** Add task-specific context (specs, requirements)
- **Implementation Phase:** Include technical context (patterns, constraints)
- **Review Phase:** Load quality and testing context

### Context Caching Strategy
```json
{
  "cache_levels": {
    "persistent": ["project_vision", "architecture_patterns"],
    "session": ["current_task", "active_files"],
    "temporary": ["search_results", "generated_content"]
  }
}
```

### Context Synchronization
- **File Changes:** Update context when project files modified
- **Task Transitions:** Refresh context for new tasks
- **Session Boundaries:** Persist important context across sessions
- **Collaboration:** Share context state between team members

## Best Practices

### Context Design
1. **Structure First:** Organize before delivering
2. **Layer Progressively:** General to specific information flow
3. **Filter Aggressively:** Include only relevant information
4. **Update Continuously:** Keep context current and accurate

### Context Delivery
1. **Match Task Complexity:** Simple tasks need simple context
2. **Respect Cognitive Limits:** Avoid information overwhelm
3. **Provide Navigation:** Help AI find specific information
4. **Enable Iteration:** Allow context refinement

### Context Maintenance
1. **Regular Audits:** Review context relevance and accuracy
2. **Usage Analytics:** Track which context elements are most valuable
3. **Feedback Loops:** Learn from AI and user interactions
4. **Version Control:** Track context evolution over time

## Troubleshooting

### Common Context Issues
- **Information Overload:** Too much context causes confusion
- **Missing Context:** Insufficient information leads to poor results
- **Stale Context:** Outdated information causes incorrect assumptions
- **Fragmented Context:** Disconnected pieces don't form coherent picture

### Resolution Strategies
- **Scope Reduction:** Narrow focus to essential information
- **Context Refresh:** Update with current project state
- **Relationship Mapping:** Show connections between context elements
- **Incremental Loading:** Add context progressively as needed

## Success Metrics

- **Context Hit Rate:** Percentage of times AI has needed information
- **Task Completion Accuracy:** How often context leads to correct outcomes
- **Context Efficiency:** Information-to-value ratio in context packages
- **User Satisfaction:** Developer feedback on context usefulness