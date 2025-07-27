---
id: github_integration
category: workflow
priority: 50
version: 1.0
description: >
  Implements comprehensive GitHub integration workflow for issue management,
  project coordination, and development lifecycle integration with AI-assisted
  development processes.
---

## Purpose

Establish seamless integration between ClaudeCode development workflows and GitHub's project management capabilities, enabling efficient issue tracking, project coordination, and collaborative development with AI assistance.

## Core Integration Philosophy

> "GitHub as the single source of truth for project state and collaboration"

This workflow treats GitHub not just as a code repository, but as the central coordination hub for all development activities, connecting issues, planning, implementation, and delivery.

## GitHub Integration Components

### Issue Management
- **Issue Creation:** Automated issue generation from specifications
- **Issue Tracking:** Progress monitoring and status updates
- **Issue Linking:** Connect related issues, PRs, and project items
- **Label Management:** Consistent categorization and prioritization

### Project Coordination
- **Milestone Planning:** Align development phases with GitHub milestones
- **Project Boards:** Visual workflow management and progress tracking
- **Release Management:** Coordinate releases with GitHub releases
- **Documentation Sync:** Keep GitHub wikis and docs current

### Development Integration
- **Branch Management:** Consistent branching strategies
- **Pull Request Workflows:** Standardized PR creation and review
- **CI/CD Integration:** Automated testing and deployment
- **Code Review Processes:** Structured review and approval workflows

## Workflow Processes

### Phase 1: Issue Creation and Planning

#### Automated Issue Generation
```markdown
1. **Analyze Specifications**
   - Parse PRD and technical specifications
   - Identify discrete work items
   - Determine dependencies and relationships

2. **Generate Issue Templates**
   - Use standardized issue templates
   - Include acceptance criteria and context
   - Set appropriate labels and assignees

3. **Create GitHub Issues**
   - Batch create related issues
   - Establish linking and dependencies
   - Add to appropriate projects and milestones
```

#### Issue Template Structure
```markdown
## Description
[Clear description of what needs to be accomplished]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Details
### Context
[Background information and current state]

### Implementation Notes
[Specific technical requirements or constraints]

### Dependencies
- Related to #[issue_number]
- Blocks #[issue_number]
- Blocked by #[issue_number]

## Definition of Done
- [ ] Implementation complete
- [ ] Tests written and passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Issue validated and closed
```

### Phase 2: Development Workflow Integration

#### Branch Management Strategy
```markdown
1. **Branch Naming Convention**
   - Feature: `feature/issue-[number]-[short-description]`
   - Bugfix: `bugfix/issue-[number]-[short-description]`
   - Hotfix: `hotfix/issue-[number]-[short-description]`

2. **Branch Creation Process**
   - Create branch from appropriate base (main/develop)
   - Link branch to issue in GitHub
   - Set up branch protection rules

3. **Branch Lifecycle**
   - Regular sync with base branch
   - Continuous integration checks
   - Review readiness validation
```

#### Pull Request Workflow
```markdown
1. **PR Creation Standards**
   - Use PR templates for consistency
   - Link to related issues
   - Include comprehensive description
   - Add appropriate reviewers

2. **PR Review Process**
   - Automated CI/CD checks
   - Code quality validation
   - Manual review requirements
   - Approval workflows

3. **PR Merge Strategy**
   - Squash commits for clean history
   - Update related issues
   - Trigger deployment processes
```

### Phase 3: Project Coordination

#### Project Board Management
```markdown
1. **Board Structure**
   - Backlog: Planned work items
   - In Progress: Active development
   - Review: Code review and testing
   - Done: Completed work

2. **Automation Rules**
   - Auto-move issues based on PR status
   - Label-based column assignment
   - Milestone progress tracking

3. **Progress Monitoring**
   - Burndown charts and velocity tracking
   - Bottleneck identification
   - Resource allocation optimization
```

#### Milestone Management
```markdown
1. **Milestone Planning**
   - Align with development phases
   - Set realistic timelines
   - Include buffer time for testing

2. **Progress Tracking**
   - Regular milestone reviews
   - Issue completion monitoring
   - Timeline adjustment protocols

3. **Release Coordination**
   - Feature freeze processes
   - Release candidate preparation
   - Production deployment coordination
```

## GitHub API Integration

### Authentication and Setup
```json
{
  "github_config": {
    "authentication": "github_token",
    "repository": "organization/repository",
    "default_branch": "main",
    "api_version": "v4"
  }
}
```

### Issue Operations
```json
{
  "issue_operations": {
    "create_issue": "POST /repos/{owner}/{repo}/issues",
    "update_issue": "PATCH /repos/{owner}/{repo}/issues/{issue_number}",
    "list_issues": "GET /repos/{owner}/{repo}/issues",
    "add_labels": "POST /repos/{owner}/{repo}/issues/{issue_number}/labels",
    "assign_users": "POST /repos/{owner}/{repo}/issues/{issue_number}/assignees"
  }
}
```

### Project Operations
```json
{
  "project_operations": {
    "create_project": "POST /repos/{owner}/{repo}/projects",
    "add_card": "POST /projects/columns/{column_id}/cards",
    "move_card": "PATCH /projects/columns/cards/{card_id}",
    "update_project": "PATCH /projects/{project_id}"
  }
}
```

## AI Command Integration

### GitHub Commands
```json
{
  "github_commands": {
    "/gh_create_issues [spec_file]": "Generate issues from specification",
    "/gh_update_status [issue_number]": "Update issue progress",
    "/gh_link_pr [pr_number] [issue_number]": "Link PR to issue",
    "/gh_create_milestone [name] [date]": "Create project milestone",
    "/gh_sync_project": "Sync project board with current state",
    "/gh_generate_release": "Create release notes and tag"
  }
}
```

### Workflow Integration Commands
```json
{
  "workflow_commands": {
    "/start_from_issue [issue_number]": "Begin development from GitHub issue",
    "/create_pr_from_branch [branch_name]": "Create PR with standard template",
    "/update_project_board": "Sync current progress to project board",
    "/close_issue_with_pr [issue_number] [pr_number]": "Link and close issue"
  }
}
```

## Templates and Standards

### Issue Templates
```markdown
## Bug Report Template
**Bug Description:** [Clear description of the bug]
**Steps to Reproduce:** [Numbered steps]
**Expected Behavior:** [What should happen]
**Actual Behavior:** [What actually happens]
**Environment:** [System details]

## Feature Request Template
**Feature Description:** [What feature is needed]
**Use Case:** [Why this feature is valuable]
**Acceptance Criteria:** [How to know when complete]
**Priority:** [High/Medium/Low]
```

### PR Templates
```markdown
## Pull Request Template
**Description:** [What this PR accomplishes]
**Related Issues:** Closes #[issue_number]
**Changes Made:** [List of key changes]
**Testing:** [How changes were tested]
**Checklist:**
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code review completed
- [ ] CI checks passing
```

## Quality Assurance

### GitHub Integration Checklist
- [ ] Issues properly linked to work items
- [ ] Branch naming follows conventions
- [ ] PRs include comprehensive descriptions
- [ ] Project boards reflect current state
- [ ] Milestones track actual progress

### Automation Validation
- [ ] Issue creation works correctly
- [ ] PR linking functions properly
- [ ] Project board updates automatically
- [ ] CI/CD integration operational
- [ ] Release processes validated

## Best Practices

### Issue Management
1. **Atomic Issues:** Each issue should represent one logical unit of work
2. **Clear Descriptions:** Issues should be understandable without context
3. **Proper Labeling:** Use consistent labels for categorization
4. **Regular Updates:** Keep issue status current throughout development
5. **Close Promptly:** Close issues when work is complete and validated

### Project Organization
1. **Consistent Structure:** Use standardized project board layouts
2. **Regular Maintenance:** Keep boards current and remove outdated items
3. **Clear Priorities:** Use labels and columns to indicate priority levels
4. **Documentation:** Maintain project documentation in GitHub wikis
5. **Team Communication:** Use GitHub discussions for team coordination

### Development Integration
1. **Branch Hygiene:** Keep branches focused and up-to-date
2. **PR Quality:** Ensure PRs are reviewable and well-documented
3. **CI/CD Reliability:** Maintain robust automated testing and deployment
4. **Review Processes:** Establish clear code review standards
5. **Release Management:** Use GitHub releases for version management

## Troubleshooting

### Common Issues
- **API Rate Limits:** Implement proper rate limiting and caching
- **Permission Issues:** Ensure proper GitHub permissions and tokens
- **Sync Problems:** Handle conflicts between local and GitHub state
- **Integration Failures:** Robust error handling for API operations

### Resolution Strategies
- **Authentication Validation:** Verify GitHub token permissions
- **State Reconciliation:** Implement sync processes for data consistency
- **Error Recovery:** Graceful handling of API failures and retries
- **Monitoring:** Track integration health and performance metrics

## Success Metrics

### Integration Effectiveness
- **Issue Tracking Accuracy:** Percentage of work items properly tracked
- **PR Completion Rate:** Successfully merged PRs vs. total created
- **Project Board Currency:** How well boards reflect actual project state
- **Release Success Rate:** Percentage of successful releases

### Team Productivity
- **Issue Resolution Time:** Average time from creation to closure
- **PR Review Time:** Average time from creation to merge
- **Release Frequency:** How often successful releases are deployed
- **Team Collaboration:** Usage of GitHub collaboration features

This GitHub integration workflow ensures seamless coordination between development activities and project management, enabling efficient collaboration and progress tracking in AI-assisted development environments.