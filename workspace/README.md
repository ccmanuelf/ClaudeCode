# ClaudeCode Workspace

This directory is where all actual development work takes place. It is completely separate from the ClaudeCode framework files to ensure clean separation of concerns and prevent interference between operational guidelines and development deliverables.

## Directory Structure

```
workspace/
├── projects/        # Full applications and major components
├── snippets/        # Small utilities and functions
├── references/      # Project-specific documentation
└── sessions/        # Session tracking and context preservation
```

## Core Principles

1. **Framework Separation** - No development work ever goes in the ClaudeCode/ directory
2. **Date-Based Organization** - All projects use YYYYMMDD naming for chronological clarity
3. **Session Tracking** - Every development session is documented for continuity
4. **Context Preservation** - Complete information maintained for handoffs and resumption

## Project Organization

### Project Naming Convention
All projects must follow this pattern:
```
[project-type]-[project-name]-YYYYMMDD
```

**Examples**:
- `react-dashboard-20241225`
- `python-data-processor-20241225`
- `php-api-endpoints-20241225`
- `js-utility-functions-20241225`

### Standard Project Structure
Each project directory should contain:
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

## Snippet Management

### Organization Pattern
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

### Snippet Documentation
Each snippet should include:
- Purpose and functionality description
- Usage examples and parameters
- Dependencies and requirements
- Creation date and context
- Related projects or use cases

## Session Management

### Session File Creation
Every development session must create or update:
```
workspace/sessions/session-YYYYMMDD-HHMM-[project-name].md
```

### Required Session Information
- Project name and workspace location
- Current objectives and goals
- Technology stack and dependencies
- Progress summary and accomplishments
- Next steps and priorities
- Context for handoff or continuation

### Session Template
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

## Reference Management

### Project References
Store project-specific documentation in:
```
workspace/references/[project-name]/
├── api-docs/            # External API documentation
├── requirements/        # Project requirements and specifications
├── research-notes/      # Investigation and planning notes
└── external-resources/  # Third-party documentation
```

### Shared References
Cross-project references and research:
```
workspace/references/shared/
├── architecture-patterns/    # Design patterns and architectures
├── best-practices/          # Coding standards and guidelines
├── tool-guides/             # Development tool documentation
└── learning-resources/      # Educational materials and tutorials
```

## Multi-Project Workflow

### Same-Day Multiple Projects
When working on multiple projects in a single day:

1. **Create separate project directories** with unique names
2. **Maintain independent session files** for each project
3. **Use project-specific configuration** and dependencies
4. **Document context switches** in session notes
5. **Keep clear separation** between project files and references

**Example Multi-Project Day**:
```
workspace/
├── projects/
│   ├── react-dashboard-20241225/
│   ├── python-scraper-20241225/
│   ├── php-api-20241225/
│   └── js-utilities-20241225/
└── sessions/
    ├── session-20241225-0900-react-dashboard.md
    ├── session-20241225-1100-python-scraper.md
    ├── session-20241225-1400-php-api.md
    └── session-20241225-1600-js-utilities.md
```

### Project Switching Protocol
1. **Save current session state** with complete documentation
2. **Commit or save** all current work
3. **Create handoff notes** for resumption
4. **Switch to target project** directory
5. **Load project context** from previous sessions
6. **Create new session file** for current work

## Workspace Maintenance

### Daily Cleanup
At the end of each development day:
- [ ] Update all session files with final status
- [ ] Commit or save all project progress
- [ ] Archive completed projects if applicable
- [ ] Clean up temporary files and artifacts
- [ ] Update project README files with current status

### Weekly Organization
Every week:
- [ ] Review and archive old session files
- [ ] Consolidate scattered snippets into organized categories
- [ ] Update reference documentation with new findings
- [ ] Clean up unused or incomplete project directories
- [ ] Backup important work to external storage

### Monthly Maintenance
Every month:
- [ ] Archive completed projects to long-term storage
- [ ] Review and optimize workspace organization
- [ ] Consolidate useful snippets into reusable libraries
- [ ] Update documentation and reference materials
- [ ] Evaluate and improve workspace structure

## Quality Assurance

### Development Standards
All workspace development must follow:
- **Framework Standards** - Guidelines from ClaudeCode/development_standards/
- **Code Quality** - Consistent formatting, documentation, and testing
- **Project Structure** - Standard directory organization and file naming
- **Session Documentation** - Complete tracking and context preservation

### Handoff Preparation
When preparing work for handoff to another AI or developer:
1. **Complete session documentation** with current status
2. **Save all work** with clear commit messages or file organization
3. **Document any uncommitted changes** or work in progress
4. **Provide clear next steps** and priorities
5. **Ensure workspace organization** follows established patterns

## Integration with ClaudeCode Framework

### Framework Compliance
The workspace must always comply with:
- **Collaboration Protocols** - AI interaction patterns from framework
- **Development Standards** - Quality requirements and coding guidelines
- **Project Management** - Progress tracking and workflow procedures

### Template Usage
Apply templates from ClaudeCode/customization_templates/ to:
- Initialize new project structures consistently
- Set up standard configuration files
- Establish documentation patterns
- Configure quality control measures

### Reference Integration
Regularly consult ClaudeCode/reference_docs/ for:
- Best practices guidance and recommendations
- Troubleshooting common development issues
- Workflow optimization strategies
- Standards compliance verification

## Troubleshooting

### Common Issues and Solutions

**Files in Wrong Location**:
- Move development work from ClaudeCode/ to workspace/
- Ensure proper directory structure is maintained

**Missing Session Context**:
- Create session files with complete project information
- Document current state and next steps clearly

**Project Naming Conflicts**:
- Use date-based naming convention consistently
- Create unique project identifiers for similar projects

**Lost Progress**:
- Implement regular session documentation
- Save work frequently with clear progress markers

**Difficult Handoffs**:
- Improve session context documentation
- Provide complete project state information
- Include clear next steps and priorities

### Recovery Procedures

**Workspace Corruption**:
1. Restore from most recent backup
2. Reorganize according to established patterns
3. Recreate missing session documentation
4. Verify framework compliance

**Missing Sessions**:
1. Review project files and commit history
2. Reconstruct session context from available information
3. Create new session files with current understanding
4. Document any gaps or uncertainties

**Context Loss**:
1. Examine project files for current state
2. Review any available documentation or comments
3. Recreate session context based on file analysis
4. Start new session with reconstructed information

## Success Metrics

### Well-Organized Workspace Demonstrates
- **Clear Structure** - Logical organization following established patterns
- **Complete Documentation** - Thorough session and project tracking
- **Easy Navigation** - Intuitive file and directory organization
- **Seamless Handoffs** - Complete context preservation for continuity
- **Efficient Development** - Minimal setup overhead for new work

### Quality Indicators
- Projects follow standard directory structure
- Session files contain complete context information
- Snippets are properly categorized and documented
- References are organized and accessible
- Multi-project work is clearly separated and tracked

---

**Remember**: This workspace is your development playground. Keep it organized, documented, and completely separate from the ClaudeCode framework to ensure smooth AI collaboration and successful project outcomes. Every file, every session, and every project should follow the established patterns to maintain consistency and enable effective teamwork.