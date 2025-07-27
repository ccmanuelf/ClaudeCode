# ClaudeCode Session Initialization

## Standard AI Collaboration Activation Prompt

Use this exact prompt to activate ClaudeCode framework guidelines in any AI conversation:

---

**🎯 ClaudeCode Framework Activation**

I'm working with the ClaudeCode Framework of Conduct for AI-human software development collaboration. Please:

1. **Read Framework Guidelines**: Review the ClaudeCode collaboration protocols, development standards, and project management guidelines in this repository
2. **Activate Workspace Management**: Use the workspace/ directory for all development work, keeping it separate from framework files
3. **Follow Session Protocols**: Implement proper session tracking and context preservation
4. **Apply Development Standards**: Follow the established coding standards, workflows, and quality guidelines

**Current Session Context**:
- Project: [Specify current project or "New Project"]
- Language/Framework: [Specify technology stack]
- Session Type: [Development/Debugging/Review/Planning]
- Workspace Location: workspace/projects/[project-name-YYYYMMDD]/

**Framework Location**: All guidelines are in ClaudeCode/ directory
**Work Location**: All development work goes in workspace/ directory

Please confirm framework activation and begin following ClaudeCode protocols.

---

## Framework Activation Checklist

When an AI partner receives this prompt, they should:

### ✅ Initial Setup
- [ ] Acknowledge ClaudeCode framework activation
- [ ] Confirm understanding of workspace separation
- [ ] Identify current session context
- [ ] Set up proper workspace organization

### ✅ Framework Discovery
- [ ] Scan collaboration_protocols/ for interaction guidelines
- [ ] Review development_standards/ for quality requirements
- [ ] Check project_management/ for workflow procedures
- [ ] Reference customization_templates/ for project-specific adaptations

### ✅ Session Configuration
- [ ] Create or resume workspace session
- [ ] Establish project-specific workspace directory
- [ ] Initialize session tracking
- [ ] Confirm technology stack and requirements

### ✅ Operational Readiness
- [ ] Apply persona and behavior guidelines
- [ ] Follow established workflows
- [ ] Implement quality guardrails
- [ ] Maintain context preservation protocols

## Quick Reference Commands

Once framework is activated, use these commands for session management:

### Workspace Commands
- `workspace create [project-name]` - Create new project workspace
- `workspace resume [project-name]` - Resume existing project
- `workspace list` - Show all active projects
- `workspace clean` - Organize and clean workspace

### Session Commands
- `session save` - Save current session context
- `session restore [session-id]` - Restore previous session
- `session handoff` - Prepare session for handoff to another AI
- `session summary` - Generate session summary

### Framework Commands
- `framework status` - Show current framework configuration
- `framework update` - Check for framework updates
- `framework customize` - Apply project-specific customizations
- `framework help` - Show detailed framework guidance

## Multi-Project Management

When working on multiple projects in the same day:

### Project Naming Convention
```
workspace/projects/
├── react-dashboard-20241225/
├── python-scraper-20241225/
├── php-api-20241225/
└── js-utilities-20241225/
```

### Session Isolation
- Each project maintains separate workspace
- Context switching requires explicit session save/restore
- Cross-project references tracked in workspace/references/

### Handoff Preparation
- Document session state in workspace/sessions/
- Create handoff summary with current progress
- Preserve all context for seamless continuation

## Framework Compliance Verification

Before beginning any development work, verify:

1. **Workspace Separation**: No development files in ClaudeCode/ directory
2. **Session Tracking**: Proper workspace/sessions/ documentation
3. **Standard Compliance**: Following development_standards/ guidelines
4. **Context Preservation**: Session state properly maintained

## AI Provider Compatibility

This initialization works with:
- Claude (Anthropic)
- ChatGPT (OpenAI)
- DeepSeek
- Gemini (Google)
- Local AI models
- Custom AI implementations

## Troubleshooting

### Framework Not Activating
- Ensure ClaudeCode directory structure is complete
- Verify all required framework files are present
- Check AI has access to read framework guidelines

### Workspace Conflicts
- Confirm workspace/ directory separation
- Verify no development files in framework directories
- Check project naming conventions are followed

### Session Continuity Issues
- Ensure session context is properly saved
- Verify handoff documentation is complete
- Check workspace/sessions/ for session state

## Success Indicators

Framework is properly activated when:
- AI acknowledges framework guidelines
- Workspace separation is maintained
- Development standards are consistently applied
- Session context is preserved across interactions
- Multi-project management works seamlessly

---

**Note**: This initialization prompt should be used at the start of every ClaudeCode session to ensure consistent AI collaboration behavior across all providers and projects.