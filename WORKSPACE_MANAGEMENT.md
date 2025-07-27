# ClaudeCode Workspace Management

## Core Principles

The ClaudeCode framework maintains strict separation between:
- **Framework Files** (ClaudeCode/ directory) - AI collaboration guidelines and standards
- **Development Work** (workspace/ directory) - All actual coding, projects, and deliverables

This separation ensures that development activities never interfere with the framework's operational guidelines.

## Directory Structure

```
ClaudeCode/                          # FRAMEWORK ONLY - Never put development work here
├── collaboration_protocols/         # How AI and humans interact
├── development_standards/           # Quality and process requirements  
├── project_management/              # Organization and tracking tools
├── reference_docs/                  # Documentation and guides
├── customization_templates/         # Adaptable templates
├── workspace/                       # DEVELOPMENT WORK ONLY
│   ├── projects/                    # Full applications and components
│   ├── snippets/                    # Small utilities and functions
│   ├── references/                  # Project-specific documentation
│   └── sessions/                    # Session tracking and context
└── [framework files...]
```

## Workspace Organization Rules

### 1. Project Naming Convention
All projects must follow the date-based naming pattern:
```
[project-type]-[project-name]-YYYYMMDD
```

**Examples**:
- `react-dashboard-20241225`
- `python-data-processor-20241225`
- `php-api-endpoints-20241225`
- `js-utility-functions-20241225`

**Rationale**: Date-based naming prevents conflicts when working on similar projects and provides clear chronological organization.

### 2. Project Structure Template
Each project should follow this internal structure:
```
workspace/projects/[project-name-YYYYMMDD]/
├── src/                 # Source code
├── docs/                # Project-specific documentation
├── tests/               # Test files
├── config/              # Configuration files
├── assets/              # Static assets (images, etc.)
├── README.md            # Project overview and setup
├── CHANGELOG.md         # Development progress log
└── SESSION_NOTES.md     # Session-specific development notes
```

### 3. Snippet Organization
Small utilities and code fragments belong in:
```
workspace/snippets/
├── [language]/
│   ├── [category]/
│   └── [utility-name-YYYYMMDD].ext
└── cross-platform/
    └── [utility-name-YYYYMMDD].ext
```

**Examples**:
- `workspace/snippets/python/data-processing/csv-parser-20241225.py`
- `workspace/snippets/javascript/dom-utils/element-finder-20241225.js`
- `workspace/snippets/cross-platform/regex-patterns-20241225.md`

## Session Management

### 1. Session Context Preservation
Every development session must create or update:
```
workspace/sessions/session-YYYYMMDD-HHMM.md
```

**Required Session Information**:
- Project name and location
- Current objectives
- Technology stack
- Progress summary
- Next steps
- Context for handoff

### 2. Session Template
```markdown
# Development Session - [Date] [Time]

## Project Context
- **Project**: [project-name]
- **Location**: workspace/projects/[project-name-YYYYMMDD]/
- **Technology**: [language/framework]
- **Session Type**: [Development/Debugging/Review/Planning]

## Objectives
- [ ] [Primary objective]
- [ ] [Secondary objective]
- [ ] [Additional tasks]

## Progress Summary
[What was accomplished this session]

## Current State
[Current status of the project]

## Next Steps
[What needs to be done next]

## Handoff Notes
[Context for next session or different AI]

## Files Modified
- [list of files changed]

## Issues Encountered
- [problems and solutions]
```

### 3. Multi-Project Session Management
When working on multiple projects in a single day:

1. **Create separate session files** for each project
2. **Use project-specific workspace directories**
3. **Maintain context isolation** between projects
4. **Document project switches** in session notes

**Example Multi-Project Day**:
```
workspace/sessions/
├── session-20241225-0900-react-dashboard.md
├── session-20241225-1100-python-scraper.md
├── session-20241225-1400-php-api.md
└── session-20241225-1600-js-utilities.md
```

## Reference Management

### 1. Project References
Store project-specific documentation in:
```
workspace/references/[project-name]/
├── api-docs/
├── requirements/
├── research-notes/
└── external-resources/
```

### 2. Cross-Project References
Shared references and research:
```
workspace/references/shared/
├── architecture-patterns/
├── best-practices/
├── tool-guides/
└── learning-resources/
```

## Workspace Maintenance

### 1. Daily Cleanup Protocol
At the end of each development day:
- [ ] Update all session files with final status
- [ ] Commit or save all project progress
- [ ] Archive completed projects
- [ ] Clean up temporary files
- [ ] Update project README files

### 2. Weekly Organization
Every week:
- [ ] Review and archive old sessions
- [ ] Consolidate scattered snippets
- [ ] Update reference documentation
- [ ] Clean up unused project directories
- [ ] Backup important work

### 3. Monthly Maintenance
Every month:
- [ ] Archive completed projects to separate storage
- [ ] Review and update workspace organization
- [ ] Consolidate useful snippets into libraries
- [ ] Update documentation and references
- [ ] Optimize workspace structure

## Conflict Prevention

### 1. Framework Isolation
**NEVER**:
- Put development code in ClaudeCode/ directory
- Modify framework files during development work
- Mix project files with framework configuration
- Store temporary files in framework directories

### 2. Project Isolation
**ALWAYS**:
- Use separate directories for each project
- Maintain project-specific configuration
- Avoid cross-project file dependencies
- Keep session contexts separate

### 3. AI Handoff Preparation
When preparing for AI handoff:
1. **Complete session documentation**
2. **Save all current progress**
3. **Document any uncommitted changes**
4. **Provide clear next steps**
5. **Ensure workspace organization is clean**

## Workspace Commands

### Project Management
```bash
# Create new project workspace
mkdir -p workspace/projects/[project-name-YYYYMMDD]/{src,docs,tests,config,assets}

# Initialize project documentation
touch workspace/projects/[project-name-YYYYMMDD]/{README.md,CHANGELOG.md,SESSION_NOTES.md}

# Create session file
touch workspace/sessions/session-$(date +%Y%m%d-%H%M)-[project-name].md
```

### Cleanup Commands
```bash
# Archive old sessions (older than 30 days)
find workspace/sessions/ -name "*.md" -mtime +30 -exec mv {} workspace/archive/sessions/ \;

# List active projects
ls -la workspace/projects/

# Show disk usage by project
du -sh workspace/projects/*
```

## Integration with Framework

### 1. Framework Compliance
The workspace must always comply with:
- **Development Standards**: Follow coding guidelines from development_standards/
- **Collaboration Protocols**: Maintain AI interaction patterns from collaboration_protocols/
- **Project Management**: Use tracking methods from project_management/

### 2. Template Usage
Apply templates from customization_templates/ to:
- Initialize new project structures
- Set up standard configurations  
- Establish consistent documentation patterns
- Configure quality control measures

### 3. Reference Integration
Regularly consult reference_docs/ for:
- Best practices guidance
- Troubleshooting common issues
- Workflow optimization
- Standards compliance verification

## Success Metrics

A well-managed workspace demonstrates:
- **Clear Separation**: No framework contamination
- **Consistent Organization**: Standard project structures
- **Complete Documentation**: Thorough session tracking
- **Easy Navigation**: Logical file organization
- **Seamless Handoffs**: Complete context preservation
- **Efficient Development**: Minimal setup overhead

## Troubleshooting

### Common Issues
1. **Files in wrong directories**: Move development work to workspace/
2. **Missing session context**: Create session files with complete information
3. **Project naming conflicts**: Use date-based naming convention
4. **Lost progress**: Implement regular session documentation
5. **Difficult handoffs**: Improve context preservation practices

### Recovery Procedures
1. **Workspace corruption**: Restore from backup, reorganize according to rules
2. **Missing sessions**: Reconstruct from project files and commit history
3. **Framework contamination**: Move development files to proper workspace locations
4. **Context loss**: Review project files and recreate session documentation

---

**Remember**: The workspace is your development playground. Keep it organized, documented, and separate from the framework to ensure smooth AI collaboration and project success.