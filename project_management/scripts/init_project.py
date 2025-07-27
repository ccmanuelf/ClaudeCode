#!/usr/bin/env python3
"""
ClaudeCode Project Initialization Script
========================================

Automates the setup of new projects with ClaudeCode AI Engineering Platform integration.
This script creates project structure, validates dependencies, and configures development
environment for optimal AI-assisted development.

Usage:
    python init_project.py --name "my-project" --type "web-app" --github
    python init_project.py --interactive
    python init_project.py --validate-only

Requirements:
    - Python 3.8+
    - uv package manager
    - git
    - Optional: GitHub CLI for repository creation
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ProjectInitializer:
    """Main class for project initialization and setup."""

    def __init__(self):
        self.claude_code_root = Path(__file__).parent.parent
        self.templates_dir = self.claude_code_root / "templates" / "project_templates"
        self.config_file = self.claude_code_root / "config.yaml"
        self.validation_errors = []
        self.warnings = []

    def validate_environment(self) -> bool:
        """Validate that all required tools and dependencies are available."""
        print("🔍 Validating development environment...")

        required_tools = {
            "python": {"command": ["python", "--version"], "min_version": "3.8"},
            "git": {"command": ["git", "--version"], "required": True},
            "uv": {"command": ["uv", "--version"], "required": True}
        }

        optional_tools = {
            "gh": {"command": ["gh", "--version"], "description": "GitHub CLI for repository management"},
            "pre-commit": {"command": ["pre-commit", "--version"], "description": "Git hooks management"}
        }

        all_good = True

        # Check required tools
        for tool, config in required_tools.items():
            if not self._check_tool_availability(tool, config):
                all_good = False
                self.validation_errors.append(f"Required tool '{tool}' is not available")

        # Check optional tools
        for tool, config in optional_tools.items():
            if not self._check_tool_availability(tool, config, required=False):
                self.warnings.append(f"Optional tool '{tool}' not found: {config['description']}")

        # Validate ClaudeCode configuration
        if not self._validate_claude_code_config():
            all_good = False

        return all_good

    def _check_tool_availability(self, tool: str, config: Dict, required: bool = True) -> bool:
        """Check if a specific tool is available and meets version requirements."""
        try:
            result = subprocess.run(
                config["command"],
                capture_output=True,
                text=True,
                check=True
            )

            if "min_version" in config:
                # Version checking logic would go here
                pass

            print(f"  ✅ {tool}: Available")
            return True

        except (subprocess.CalledProcessError, FileNotFoundError):
            status = "❌" if required else "⚠️"
            print(f"  {status} {tool}: Not available")
            return False

    def _validate_claude_code_config(self) -> bool:
        """Validate ClaudeCode configuration integrity."""
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)

            # Check for required sections
            required_sections = ['persona', 'workflows', 'behaviors', 'guardrails']
            for section in required_sections:
                if section not in config:
                    self.validation_errors.append(f"Missing required config section: {section}")
                    return False

            print("  ✅ ClaudeCode configuration: Valid")
            return True

        except Exception as e:
            self.validation_errors.append(f"ClaudeCode config validation failed: {str(e)}")
            return False

    def create_project_structure(self, project_name: str, project_type: str, target_dir: Path) -> bool:
        """Create the standard project directory structure."""
        print(f"🏗️ Creating project structure for '{project_name}'...")

        # Define project structure based on type
        structures = {
            "web-app": {
                "src": ["app", "api", "utils"],
                "tests": ["unit", "integration", "e2e"],
                "docs": ["architecture", "api", "deployment"],
                "config": [],
                "scripts": ["dev", "build", "deploy"],
                "static": ["css", "js", "images"],
                ".github": ["workflows", "ISSUE_TEMPLATE", "PULL_REQUEST_TEMPLATE"]
            },
            "api-service": {
                "src": ["handlers", "models", "services", "utils"],
                "tests": ["unit", "integration", "performance"],
                "docs": ["api", "architecture", "deployment"],
                "config": ["environments"],
                "scripts": ["deployment", "migration"],
                ".github": ["workflows"]
            },
            "data-science": {
                "src": ["data", "models", "analysis", "utils"],
                "tests": ["unit", "integration"],
                "notebooks": ["exploratory", "experiments"],
                "data": ["raw", "processed", "external"],
                "docs": ["methodology", "results"],
                "config": [],
                "scripts": ["preprocessing", "training", "evaluation"]
            },
            "library": {
                "src": [project_name.replace("-", "_")],
                "tests": ["unit", "integration"],
                "docs": ["api", "examples", "tutorials"],
                "examples": [],
                "scripts": ["build", "release"],
                ".github": ["workflows"]
            }
        }

        structure = structures.get(project_type, structures["web-app"])

        try:
            # Create main project directory
            target_dir.mkdir(parents=True, exist_ok=True)

            # Create directory structure
            for main_dir, subdirs in structure.items():
                main_path = target_dir / main_dir
                main_path.mkdir(exist_ok=True)

                for subdir in subdirs:
                    (main_path / subdir).mkdir(parents=True, exist_ok=True)

            print(f"  ✅ Directory structure created")
            return True

        except Exception as e:
            print(f"  ❌ Failed to create structure: {str(e)}")
            return False

    def initialize_git_repository(self, project_dir: Path, project_name: str) -> bool:
        """Initialize git repository with proper configuration."""
        print("📦 Initializing git repository...")

        try:
            # Initialize git repo
            subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)

            # Create .gitignore
            gitignore_content = self._generate_gitignore()
            (project_dir / ".gitignore").write_text(gitignore_content)

            # Create initial README
            readme_content = self._generate_readme(project_name)
            (project_dir / "README.md").write_text(readme_content)

            # Initial commit
            subprocess.run(["git", "add", "."], cwd=project_dir, check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial commit: Project structure created"],
                cwd=project_dir, check=True, capture_output=True
            )

            print("  ✅ Git repository initialized")
            return True

        except subprocess.CalledProcessError as e:
            print(f"  ❌ Git initialization failed: {str(e)}")
            return False

    def setup_python_environment(self, project_dir: Path, project_name: str, project_type: str) -> bool:
        """Set up Python environment with uv and dependencies."""
        print("🐍 Setting up Python environment...")

        try:
            # Initialize uv project
            subprocess.run(["uv", "init", "--name", project_name], cwd=project_dir, check=True)

            # Generate pyproject.toml content
            pyproject_content = self._generate_pyproject_toml(project_name, project_type)
            (project_dir / "pyproject.toml").write_text(pyproject_content)

            # Install base dependencies
            base_deps = ["pytest", "pytest-cov", "black", "ruff", "pre-commit"]
            for dep in base_deps:
                subprocess.run(["uv", "add", "--group", "dev", dep], cwd=project_dir, check=True)

            print("  ✅ Python environment configured")
            return True

        except subprocess.CalledProcessError as e:
            print(f"  ❌ Python setup failed: {str(e)}")
            return False

    def setup_claude_code_integration(self, project_dir: Path, project_name: str) -> bool:
        """Set up ClaudeCode integration files."""
        print("⚡ Setting up ClaudeCode integration...")

        try:
            # Create claude.md file
            claude_md_content = self._generate_claude_md(project_name)
            (project_dir / "claude.md").write_text(claude_md_content)

            # Create plan.md file
            plan_md_content = self._generate_plan_md(project_name)
            (project_dir / "plan.md").write_text(plan_md_content)

            # Create todo.md file
            todo_md_content = self._generate_todo_md(project_name)
            (project_dir / "todo.md").write_text(todo_md_content)

            # Create specs directory
            specs_dir = project_dir / "specs"
            specs_dir.mkdir(exist_ok=True)

            print("  ✅ ClaudeCode integration configured")
            return True

        except Exception as e:
            print(f"  ❌ ClaudeCode integration failed: {str(e)}")
            return False

    def setup_quality_tools(self, project_dir: Path) -> bool:
        """Set up code quality and testing tools."""
        print("🛡️ Setting up quality assurance tools...")

        try:
            # Create pre-commit config
            precommit_config = self._generate_precommit_config()
            (project_dir / ".pre-commit-config.yaml").write_text(precommit_config)

            # Create pytest config
            pytest_config = self._generate_pytest_config()
            (project_dir / "pytest.ini").write_text(pytest_config)

            # Install pre-commit hooks
            subprocess.run(["pre-commit", "install"], cwd=project_dir, check=True, capture_output=True)

            print("  ✅ Quality tools configured")
            return True

        except subprocess.CalledProcessError as e:
            print(f"  ❌ Quality tools setup failed: {str(e)}")
            return False

    def create_github_repository(self, project_dir: Path, project_name: str) -> bool:
        """Create GitHub repository if GitHub CLI is available."""
        print("🐙 Creating GitHub repository...")

        try:
            # Check if gh is available
            subprocess.run(["gh", "--version"], check=True, capture_output=True)

            # Create repository
            subprocess.run(
                ["gh", "repo", "create", project_name, "--public", "--source", "."],
                cwd=project_dir, check=True, capture_output=True
            )

            print("  ✅ GitHub repository created")
            return True

        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  ⚠️ GitHub CLI not available or repository creation failed")
            return False

    def interactive_setup(self) -> Dict:
        """Run interactive setup wizard."""
        print("🧙 ClaudeCode Interactive Project Setup Wizard")
        print("=" * 50)

        # Project name
        project_name = input("Project name: ").strip()
        while not project_name or not project_name.replace("-", "").replace("_", "").isalnum():
            print("Please enter a valid project name (alphanumeric, hyphens, underscores)")
            project_name = input("Project name: ").strip()

        # Project type
        print("\nAvailable project types:")
        types = ["web-app", "api-service", "data-science", "library"]
        for i, ptype in enumerate(types, 1):
            print(f"  {i}. {ptype}")

        while True:
            try:
                choice = int(input("Select project type (1-4): "))
                if 1 <= choice <= 4:
                    project_type = types[choice - 1]
                    break
            except ValueError:
                pass
            print("Please enter a number between 1 and 4")

        # Target directory
        default_dir = Path.cwd() / project_name
        target_dir = input(f"Target directory [{default_dir}]: ").strip()
        if not target_dir:
            target_dir = default_dir
        else:
            target_dir = Path(target_dir)

        # GitHub integration
        create_github = input("Create GitHub repository? (y/N): ").strip().lower() == 'y'

        return {
            "name": project_name,
            "type": project_type,
            "target_dir": target_dir,
            "create_github": create_github
        }

    def run_full_initialization(self, config: Dict) -> bool:
        """Run the complete project initialization process."""
        print(f"\n🚀 Initializing project '{config['name']}'...")
        print("=" * 60)

        success = True

        # Validate environment
        if not self.validate_environment():
            print("\n❌ Environment validation failed:")
            for error in self.validation_errors:
                print(f"  • {error}")
            return False

        if self.warnings:
            print("\n⚠️ Warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")

        # Create project structure
        if not self.create_project_structure(
            config["name"], config["type"], config["target_dir"]
        ):
            success = False

        # Initialize git
        if success and not self.initialize_git_repository(config["target_dir"], config["name"]):
            success = False

        # Setup Python environment
        if success and not self.setup_python_environment(
            config["target_dir"], config["name"], config["type"]
        ):
            success = False

        # Setup ClaudeCode integration
        if success and not self.setup_claude_code_integration(config["target_dir"], config["name"]):
            success = False

        # Setup quality tools
        if success and not self.setup_quality_tools(config["target_dir"]):
            success = False

        # Create GitHub repository if requested
        if success and config.get("create_github", False):
            self.create_github_repository(config["target_dir"], config["name"])

        return success

    # Helper methods for generating file content

    def _generate_gitignore(self) -> str:
        """Generate appropriate .gitignore content."""
        return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
*.log
.coverage
htmlcov/
.pytest_cache/
.ruff_cache/

# Secrets
*.key
*.pem
secrets.yaml
.env.local
"""

    def _generate_readme(self, project_name: str) -> str:
        """Generate initial README.md content."""
        return f"""# {project_name}

## Overview

This project was initialized with the ClaudeCode AI Engineering Platform, providing
comprehensive development workflows, testing frameworks, and AI-assisted development
capabilities.

## Quick Start

### Prerequisites

- Python 3.8+
- uv package manager
- git

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd {project_name}
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

4. Run tests:
   ```bash
   uv run pytest
   ```

## Development

This project follows ClaudeCode AI Engineering methodologies:

- **Specs-Driven Development**: Create detailed specifications before implementation
- **Test-Driven Development**: Write tests first, then implement
- **Context Engineering**: Maintain clear, structured project context
- **Quality Gates**: Automated quality assurance at every step

### Key Files

- `claude.md`: AI development partner configuration
- `plan.md`: Project planning and architecture documentation
- `todo.md`: Task tracking and progress management
- `specs/`: Detailed specifications for features and components

### Development Workflow

1. Review current tasks in `todo.md`
2. Create or update specifications in `specs/`
3. Write tests for new functionality
4. Implement features following TDD principles
5. Ensure all quality gates pass
6. Update documentation and planning files

## Project Structure

```
{project_name}/
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── specs/                  # Feature specifications
├── config/                 # Configuration files
├── scripts/                # Utility scripts
├── claude.md              # AI development configuration
├── plan.md                # Project planning
└── todo.md                # Task tracking
```

## Contributing

This project uses ClaudeCode development standards:

1. All changes must include tests
2. Code must pass all quality gates
3. Specifications must be updated for new features
4. Documentation must be kept current

## License

[Add your license information here]
"""

    def _generate_claude_md(self, project_name: str) -> str:
        """Generate claude.md configuration file."""
        return f"""# Claude Development Partner Configuration

## Project: {project_name}

This file configures the AI development partner for this project, establishing
context, preferences, and development standards.

## Project Context

### Overview
[Describe the project purpose, goals, and target audience]

### Technical Stack
[List the main technologies, frameworks, and tools used]

### Architecture
[Describe the high-level system architecture and design patterns]

## Development Standards

### Code Quality
- Follow ClaudeCode development standards
- Maintain test coverage above 80%
- Use pre-commit hooks for quality assurance
- Write self-documenting code with clear comments

### Testing Strategy
- Practice Test-Driven Development (TDD)
- Write unit tests for all business logic
- Include integration tests for component interactions
- Add end-to-end tests for critical user journeys

### Git Workflow
- Use conventional commit messages
- Create feature branches for new work
- Require pre-commit hooks to pass
- Use pull requests for code review

## AI Development Preferences

### Communication Style
- Provide detailed explanations for complex concepts
- Include code examples and practical demonstrations
- Ask clarifying questions when requirements are unclear
- Suggest best practices and alternative approaches

### Workflow Integration
- Follow specs-driven development methodology
- Use context engineering for optimal information flow
- Integrate with project planning and task management
- Maintain session continuity across development activities

## Project-Specific Guidelines

### Naming Conventions
[Define naming patterns for files, functions, classes, etc.]

### Error Handling
[Specify error handling patterns and logging standards]

### Documentation
[Define documentation requirements and formats]

### Dependencies
[List policies for adding and managing dependencies]

## Quick Commands

- `/analyze`: Perform deep analysis of current task or problem
- `/spec`: Create or review feature specifications
- `/tdd`: Start test-driven development cycle
- `/review`: Review code quality and suggest improvements
- `/plan`: Update project planning and task breakdown
- `/context`: Load relevant project context for current task

## Session Management

This project supports advanced session management:
- Progress tracking across development sessions
- Context preservation and restoration
- Decision documentation and rationale capture
- Knowledge accumulation and learning retention

---

*This configuration enables optimal AI-assisted development using ClaudeCode methodologies.*
"""

    def _generate_plan_md(self, project_name: str) -> str:
        """Generate initial plan.md file."""
        return f"""# {project_name} - Development Plan

## Project Vision

### Problem Statement
[Describe the problem this project solves]

### Success Metrics
[Define how success will be measured]

### Target Timeline
[Outline major milestones and deadlines]

## Technical Architecture

### System Overview
[High-level architecture description]

### Component Breakdown
[List major system components and their responsibilities]

### Data Model
[Describe key data structures and relationships]

### Technology Decisions
[Document technology choices and rationale]

## Development Phases

### Phase 1: Foundation
- [ ] Project setup and configuration
- [ ] Core architecture implementation
- [ ] Basic testing framework
- [ ] CI/CD pipeline setup

### Phase 2: Core Features
- [ ] Feature 1: [Description]
- [ ] Feature 2: [Description]
- [ ] Feature 3: [Description]
- [ ] Integration testing

### Phase 3: Enhancement
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Documentation completion
- [ ] Deployment preparation

### Phase 4: Delivery
- [ ] User acceptance testing
- [ ] Production deployment
- [ ] Monitoring and alerting
- [ ] Knowledge transfer

## Risk Management

### Technical Risks
[Identify potential technical challenges and mitigation strategies]

### Timeline Risks
[Consider schedule risks and contingency plans]

### Resource Risks
[Address potential resource constraints]

## Quality Gates

### Code Quality
- Minimum 80% test coverage
- All pre-commit hooks passing
- Code review approval required
- Documentation up to date

### Feature Completion
- All acceptance criteria met
- Tests written and passing
- Performance benchmarks met
- Security review completed

## Decision Log

### [Date] - Technology Stack Selection
**Decision**: [What was decided]
**Rationale**: [Why this choice was made]
**Alternatives**: [What other options were considered]
**Impact**: [How this affects the project]

---

*This plan follows ClaudeCode specs-driven development methodology for systematic project execution.*
"""

    def _generate_todo_md(self, project_name: str) -> str:
        """Generate initial todo.md file."""
        return f"""# {project_name} - Task Tracking

## Current Sprint

### In Progress
- [ ] Project initialization and setup
- [ ] Development environment configuration
- [ ] Quality assurance tools setup

### Planned
- [ ] Create initial project specifications
- [ ] Set up continuous integration
- [ ] Implement core architecture
- [ ] Write initial test suite

### Blocked
[No blocked items currently]

## Backlog

### High Priority
- [ ] Define detailed project requirements
- [ ] Create user story mapping
- [ ] Design system architecture
- [ ] Set up deployment pipeline

### Medium Priority
- [ ] Performance benchmarking setup
- [ ] Security assessment framework
- [ ] Documentation framework
- [ ] Monitoring and alerting setup

### Low Priority
- [ ] Developer experience improvements
- [ ] Advanced tooling integration
- [ ] Optimization opportunities
- [ ] Future enhancement planning

## Completed

### {datetime.now().strftime('%Y-%m-%d')}
- [x] Project structure created
- [x] Git repository initialized
- [x] Python environment configured
- [x] ClaudeCode integration setup
- [x] Quality tools configured

## Notes

### Recent Decisions
- Chose ClaudeCode AI Engineering Platform for development methodology
- Implemented TDD workflow with comprehensive testing requirements
- Set up automated quality gates and pre-commit hooks

### Upcoming Focus
- Prioritize specs-driven development for clear requirements
- Establish GitHub integration for project management
- Create comprehensive test coverage from the start

### Lessons Learned
[Document insights and learnings as the project progresses]

---

*Task tracking integrated with ClaudeCode session management for optimal development flow.*
"""

    def _generate_pyproject_toml(self, project_name: str, project_type: str) -> str:
        """Generate pyproject.toml configuration."""
        package_name = project_name.replace("-", "_")

        return f'''[project]
name = "{project_name}"
version = "0.1.0"
description = "Project created with ClaudeCode AI Engineering Platform"
authors = [
    {{name = "Your Name", email = "your.email@example.com"}},
]
dependencies = []
readme = "README.md"
requires-python = ">= 3.8"

[project.scripts]
{package_name} = "{package_name}.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = [
    "tests",
]
python_files = [
    "test_*.py",
    "*_test.py",
]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov={package_name}",
    "--cov-report=term-missing:skip-covered",
    "--cov-report=html:htmlcov",
    "--cov-report=xml",
]

[tool.coverage.run]
source = ["{package_name}"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if __name__ == .__main__.:",
    "raise AssertionError",
    "raise NotImplementedError",
]

[tool.ruff]
target-version = "py38"
line-length = 88
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501", # line too long, handled by black
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]

[tool.black]
target-version = ['py38']
include = '\\.pyi?$'
extend-exclude = '''
/(
  # directories
  \\.eggs
  | \\.git
  | \\.hg
  | \\.mypy_cache
  | \\.tox
  | \\.venv
  | build
  | dist
)/
'''

[tool.mypy]
python_version = "3.8"
check_untyped_defs = true
disallow_any_generics = true
disallow_incomplete_defs = true
disallow_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
'''

    def _generate_precommit_config(self) -> str:
        """Generate pre-commit configuration."""
        return """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-toml
      - id: check-json
      - id: debug-statements
      - id: mixed-line-ending

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.0.287
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: uv run pytest
        language: system
        pass_filenames: false
        always_run: true
"""

    def _generate_pytest_config(self) -> str:
        """Generate pytest configuration."""
        return """[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --strict-config
    --verbose
    --tb=short
    --cov-report=term-missing:skip-covered
    --cov-report=html:htmlcov
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
"""


def main():
    """Main entry point for the project initialization script."""
    parser = argparse.ArgumentParser(
        description="Initialize new project with ClaudeCode AI Engineering Platform"
    )
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--type", choices=["web-app", "api-service", "data-science", "library"],
                       help="Project type")
    parser.add_argument("--target-dir", help="Target directory for project")
    parser.add_argument("--github", action="store_true", help="Create GitHub repository")
    parser.add_argument("--interactive", action="store_true", help="Run interactive setup")
    parser.add_argument("--validate-only", action="store_true", help="Only validate environment")

    args = parser.parse_args()

    initializer = ProjectInitializer()

    # Validate-only mode
    if args.validate_only:
        success = initializer.validate_environment()
        if success:
            print("\n✅ Environment validation passed!")
        sys.exit(0 if success else 1)

    # Interactive mode
    if args.interactive:
        config = initializer.interactive_setup()
    else:
        # Command-line mode
        if not args.name:
            print("Error: Project name is required (use --name or --interactive)")
            sys.exit(1)

        config = {
            "name": args.name,
            "type": args.type or "web-app",
            "target_dir": Path(args.target_dir) if args.target_dir else Path.cwd() / args.name,
            "create_github": args.github
        }

    # Run initialization
    success = initializer.run_full_initialization(config)

    if success:
        print(f"\n🎉 Project '{config['name']}' initialized successfully!")
        print(f"📁 Location: {config['target_dir'].absolute()}")
        print("\n🚀 Next steps:")
        print(f"  1. cd {config['target_dir']}")
        print("  2. Review and update claude.md with project-specific information")
        print("  3. Create initial specifications in specs/ directory")
        print("  4. Start development with: uv run pytest")
        print("\n💡 Use ClaudeCode AI methodologies for optimal development experience!")
    else:
        print(f"\n❌ Project initialization failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
