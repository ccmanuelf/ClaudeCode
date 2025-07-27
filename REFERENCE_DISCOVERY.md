# ClaudeCode Reference Discovery Protocol

## Overview

The Reference Discovery Protocol ensures that AI partners systematically identify, access, and utilize all available documentation and resources before beginning any development work. This prevents redundant effort and ensures compliance with established standards.

## Discovery Sequence

### Phase 1: Framework Structure Scan
AI must first identify the complete ClaudeCode framework structure:

```
ClaudeCode/
├── collaboration_protocols/     # AI interaction guidelines
├── development_standards/       # Quality and process requirements
├── project_management/          # Organization and tracking tools
├── reference_docs/             # Documentation and guides
├── customization_templates/    # Adaptable templates
└── workspace/                  # Development work area
```

**Required Actions**:
1. Confirm framework directory exists
2. Verify all protocol directories are present
3. Identify any custom additions or modifications
4. Note framework version or customization level

### Phase 2: Collaboration Protocols Discovery
Scan `collaboration_protocols/` for interaction guidelines:

**Subdirectories to Check**:
- `persona/` - AI personality and behavior specifications
- `prompts/` - Standard interaction prompts and responses
- `behaviors/` - Specific behavioral guidelines and constraints

**Discovery Process**:
```markdown
1. List all files in collaboration_protocols/
2. Read persona configuration files
3. Load standard prompts and responses
4. Review behavioral constraints and guidelines
5. Note any project-specific customizations
```

**Key Information to Extract**:
- Communication style preferences
- Response formatting requirements
- Interaction patterns and workflows
- Error handling procedures
- Escalation protocols

### Phase 3: Development Standards Discovery
Scan `development_standards/` for quality requirements:

**Subdirectories to Check**:
- `guardrails/` - Quality control and safety measures
- `workflows/` - Development process procedures
- `templates/` - Code and project templates
- `command_templates/` - Standard operational procedures
- `prd/` - Product requirements and specifications

**Discovery Process**:
```markdown
1. Identify coding standards for target language/framework
2. Review quality control measures and requirements
3. Load workflow procedures for development lifecycle
4. Access templates for project initialization
5. Review command templates for common operations
6. Check PRD specifications if available
```

**Key Standards to Note**:
- Code formatting and style guidelines
- Testing requirements and procedures
- Documentation standards
- Review and approval processes
- Security and safety constraints

### Phase 4: Project Management Discovery
Scan `project_management/` for organizational tools:

**Subdirectories to Check**:
- `progress_tracking/` - Progress monitoring and reporting
- `scripts/` - Automation and utility scripts

**Discovery Process**:
```markdown
1. Review progress tracking methodologies
2. Identify available automation scripts
3. Understand reporting requirements
4. Note project lifecycle management tools
5. Check for custom workflow automations
```

**Management Tools to Identify**:
- Progress tracking templates
- Status reporting formats
- Milestone and deadline management
- Resource allocation guidelines
- Quality assurance checkpoints

### Phase 5: Reference Documentation Discovery
Scan `reference_docs/` for comprehensive guides:

**Expected Documentation**:
- `docs/USAGE_EXAMPLES.md` - Complete workflow examples
- `docs/BEST_PRACTICES.md` - Optimization strategies
- `docs/TROUBLESHOOTING.md` - Problem resolution guides
- `docs/QUICK_START.md` - Getting started procedures
- `docs/CONFIGURATION_VALIDATION.md` - Config management

**Discovery Process**:
```markdown
1. Catalog all available documentation
2. Read quick start guides first
3. Review usage examples for similar projects
4. Study best practices for target technology
5. Bookmark troubleshooting resources
6. Note configuration management procedures
```

**Documentation Priority**:
1. **Quick Start** - Immediate setup procedures
2. **Usage Examples** - Real-world implementation patterns
3. **Best Practices** - Optimization and quality guidelines
4. **Troubleshooting** - Problem resolution resources
5. **Configuration** - Setup and customization guidance

### Phase 6: Customization Templates Discovery
Scan `customization_templates/` for adaptable resources:

**Subdirectories to Check**:
- `examples/configurations/` - Project setup templates
- `examples/scenarios/` - Real-world workflow examples

**Discovery Process**:
```markdown
1. Identify templates matching current project type
2. Review configuration examples for technology stack
3. Study scenario examples for similar use cases
4. Note customization patterns and options
5. Identify reusable components and patterns
```

**Templates to Prioritize**:
- Project initialization templates
- Configuration file templates
- Workflow scenario examples
- Integration pattern examples
- Testing and quality assurance templates

## Context Integration

### Information Synthesis
After discovery, AI must synthesize found information:

```markdown
## Framework Context Summary
- **Communication Style**: [extracted from persona/]
- **Quality Standards**: [extracted from guardrails/]
- **Workflow Process**: [extracted from workflows/]
- **Available Templates**: [list from templates/]
- **Reference Guides**: [list from reference_docs/]
- **Custom Configurations**: [any customizations found]
```

### Priority Ranking
Rank discovered resources by relevance to current task:

1. **Critical** - Must follow (guardrails, workflows)
2. **Important** - Should apply (best practices, templates)
3. **Reference** - Consult as needed (examples, troubleshooting)
4. **Optional** - Use if applicable (customizations, advanced features)

### Gap Identification
Note any missing or unclear information:
- Required standards not found
- Incomplete documentation
- Missing templates for current technology
- Unclear workflow procedures
- Conflicting guidelines

## Workspace Context Discovery

### Current Project Assessment
If resuming existing work, discover workspace context:

```markdown
workspace/projects/[project-name-YYYYMMDD]/
├── README.md           # Project overview and current status
├── CHANGELOG.md        # Development history and progress
├── SESSION_NOTES.md    # Session-specific context
└── [project files]    # Current implementation state
```

### Session History Review
Check for previous session context:

```markdown
workspace/sessions/
├── session-[date]-[time]-[project].md
└── [previous session files]
```

**Session Context to Extract**:
- Previous objectives and progress
- Current implementation state
- Known issues or blockers
- Next planned steps
- Handoff context from previous AI

### Reference Materials Check
Identify project-specific references:

```markdown
workspace/references/[project-name]/
├── api-docs/          # External API documentation
├── requirements/      # Project requirements and specs
├── research-notes/    # Investigation and planning notes
└── external-resources/ # Third-party documentation
```

## Discovery Validation

### Completeness Check
Verify all required information has been discovered:

- [ ] Framework structure identified
- [ ] Collaboration protocols loaded
- [ ] Development standards understood  
- [ ] Project management tools identified
- [ ] Reference documentation cataloged
- [ ] Customization templates available
- [ ] Workspace context established
- [ ] Session history reviewed

### Consistency Verification
Ensure discovered information is consistent:

- [ ] No conflicting guidelines between directories
- [ ] Templates match development standards
- [ ] Workflow procedures align with collaboration protocols
- [ ] Project requirements match available templates
- [ ] Session context aligns with project state

### Missing Information Protocol
If critical information is missing:

1. **Document the gap** in session notes
2. **Request clarification** from human collaborator
3. **Use closest available alternative** from templates
4. **Proceed with standard practices** if no guidance exists
5. **Flag for framework improvement** in next iteration

## Discovery Output Format

### Summary Report Template
```markdown
# Reference Discovery Summary

## Framework Status
- **Version**: [identified version or customization level]
- **Completeness**: [percentage of expected files found]
- **Customizations**: [list any custom additions]

## Collaboration Context
- **Persona**: [communication style and preferences]
- **Interaction Patterns**: [standard prompts and responses]
- **Behavioral Guidelines**: [constraints and requirements]

## Development Standards
- **Language/Framework**: [specific standards for current project]
- **Quality Requirements**: [testing, documentation, review standards]
- **Templates Available**: [list applicable templates]

## Project Management
- **Progress Tracking**: [methodology and tools available]
- **Workflow Process**: [development lifecycle procedures]
- **Automation Scripts**: [available utilities and tools]

## Reference Resources
- **Documentation**: [list of available guides and examples]
- **Best Practices**: [optimization and quality guidelines]
- **Troubleshooting**: [problem resolution resources]

## Workspace Context
- **Current Project**: [name and location]
- **Project Status**: [current state and progress]
- **Session History**: [previous work and context]
- **Next Steps**: [identified priorities and objectives]

## Gaps and Clarifications Needed
- [list any missing information]
- [questions for human collaborator]
- [assumptions being made due to missing data]
```

## Automated Discovery Implementation

### Discovery Script Template
```python
def discover_claudecode_context():
    """
    Automated reference discovery for ClaudeCode framework
    """
    discovery_report = {
        'framework_structure': scan_framework_directories(),
        'collaboration_protocols': load_collaboration_guidelines(),
        'development_standards': extract_quality_requirements(),
        'project_management': identify_management_tools(),
        'reference_docs': catalog_documentation(),
        'customization_templates': list_available_templates(),
        'workspace_context': assess_current_workspace(),
        'session_history': review_previous_sessions()
    }
    
    validate_discovery_completeness(discovery_report)
    return synthesis_context_summary(discovery_report)
```

### Integration with AI Initialization
Discovery should be triggered automatically when:
- New AI session begins
- Framework activation prompt is received
- Project context changes
- Handoff between AI partners occurs
- Major framework updates detected

## Success Criteria

### Effective Discovery Demonstrates
- **Complete Framework Awareness** - All available resources identified
- **Contextual Understanding** - Guidelines applied appropriately to current task
- **Workflow Integration** - Discovery results seamlessly integrated into work process
- **Gap Management** - Missing information handled appropriately
- **Efficiency** - Discovery completed quickly without disrupting development flow

### Discovery Quality Metrics
- **Coverage**: Percentage of available resources discovered
- **Accuracy**: Correct interpretation of discovered guidelines
- **Relevance**: Focus on information applicable to current task
- **Speed**: Discovery completed within reasonable time frame
- **Integration**: Discovered context properly applied to development work

---

**Note**: This protocol ensures that every AI partner has complete situational awareness before beginning development work, leading to consistent, high-quality collaboration that builds on previous work and follows established standards.