#!/usr/bin/env python3
"""
ClaudeCode Configuration Validation System
==========================================

Validates ClaudeCode configuration integrity, checks file references,
and ensures system consistency across all components.

Usage:
    python validate_config.py
    python validate_config.py --fix-auto
    python validate_config.py --detailed
    python validate_config.py --export-report validation_report.json

Features:
    - Cross-reference validation between config.yaml and actual files
    - YAML/JSON syntax validation
    - File existence and accessibility checks
    - Priority conflict detection
    - Circular dependency detection
    - Auto-fix capabilities for common issues
"""

import argparse
import json
import os
import re
import sys
import yaml
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union


class ValidationError:
    """Represents a validation error with severity and context."""

    def __init__(self, severity: str, category: str, message: str,
                 file_path: Optional[str] = None, fix_suggestion: Optional[str] = None):
        self.severity = severity  # 'critical', 'error', 'warning', 'info'
        self.category = category
        self.message = message
        self.file_path = file_path
        self.fix_suggestion = fix_suggestion
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            'severity': self.severity,
            'category': self.category,
            'message': self.message,
            'file_path': self.file_path,
            'fix_suggestion': self.fix_suggestion,
            'timestamp': self.timestamp
        }


class ConfigValidator:
    """Main configuration validation class."""

    def __init__(self, claude_code_root: Path):
        self.root = claude_code_root
        self.config_file = self.root / "config.yaml"
        self.agent_config_dir = self.root / "agent-config"
        self.errors: List[ValidationError] = []
        self.config_data: Optional[Dict] = None
        self.file_references: Dict[str, Set[str]] = defaultdict(set)
        self.priority_map: Dict[str, int] = {}

    def validate_all(self) -> bool:
        """Run comprehensive validation of all components."""
        print("🔍 Starting ClaudeCode configuration validation...")

        success = True

        # Core validation steps
        if not self._validate_config_file_exists():
            return False

        if not self._load_and_validate_config_syntax():
            return False

        if not self._validate_directory_structure():
            success = False

        if not self._validate_file_references():
            success = False

        if not self._validate_component_files():
            success = False

        if not self._validate_priorities():
            success = False

        if not self._validate_dependencies():
            success = False

        self._validate_best_practices()

        return success and not self._has_critical_errors()

    def _validate_config_file_exists(self) -> bool:
        """Check if main config file exists and is readable."""
        if not self.config_file.exists():
            self.errors.append(ValidationError(
                'critical', 'file_missing',
                f"Main configuration file not found: {self.config_file}",
                fix_suggestion="Create config.yaml in the ClaudeCode root directory"
            ))
            return False

        if not self.config_file.is_file():
            self.errors.append(ValidationError(
                'critical', 'file_type',
                f"Configuration path is not a file: {self.config_file}"
            ))
            return False

        try:
            with open(self.config_file, 'r') as f:
                f.read()
        except PermissionError:
            self.errors.append(ValidationError(
                'critical', 'file_permissions',
                f"Cannot read configuration file due to permissions: {self.config_file}"
            ))
            return False
        except Exception as e:
            self.errors.append(ValidationError(
                'critical', 'file_access',
                f"Cannot access configuration file: {str(e)}"
            ))
            return False

        return True

    def _load_and_validate_config_syntax(self) -> bool:
        """Load and validate YAML syntax of config file."""
        try:
            with open(self.config_file, 'r') as f:
                self.config_data = yaml.safe_load(f)

            if not isinstance(self.config_data, dict):
                self.errors.append(ValidationError(
                    'critical', 'config_format',
                    "Configuration file must contain a YAML dictionary at root level"
                ))
                return False

        except yaml.YAMLError as e:
            self.errors.append(ValidationError(
                'critical', 'yaml_syntax',
                f"YAML syntax error in config file: {str(e)}",
                fix_suggestion="Fix YAML syntax errors using a YAML validator"
            ))
            return False
        except Exception as e:
            self.errors.append(ValidationError(
                'critical', 'config_load',
                f"Failed to load configuration: {str(e)}"
            ))
            return False

        print("  ✅ Configuration file syntax valid")
        return True

    def _validate_directory_structure(self) -> bool:
        """Validate expected directory structure exists."""
        required_dirs = [
            "agent-config",
            "agent-config/persona",
            "agent-config/prompts",
            "agent-config/guardrails",
            "agent-config/behaviors",
            "agent-config/workflows",
            "agent-config/templates"
        ]

        optional_dirs = [
            "features",
            "logs",
            "tasks",
            "scripts",
            "agent-config/command_templates",
            "agent-config/prd"
        ]

        success = True

        for dir_path in required_dirs:
            full_path = self.root / dir_path
            if not full_path.exists():
                self.errors.append(ValidationError(
                    'error', 'missing_directory',
                    f"Required directory missing: {dir_path}",
                    fix_suggestion=f"Create directory: mkdir -p {full_path}"
                ))
                success = False
            elif not full_path.is_dir():
                self.errors.append(ValidationError(
                    'error', 'not_directory',
                    f"Path exists but is not a directory: {dir_path}"
                ))
                success = False

        for dir_path in optional_dirs:
            full_path = self.root / dir_path
            if not full_path.exists():
                self.errors.append(ValidationError(
                    'info', 'optional_directory',
                    f"Optional directory not found: {dir_path}",
                    fix_suggestion=f"Consider creating: mkdir -p {full_path}"
                ))

        if success:
            print("  ✅ Directory structure valid")

        return success

    def _validate_file_references(self) -> bool:
        """Validate all file references in config exist and are accessible."""
        if not self.config_data:
            return False

        success = True

        # Define sections that contain file references
        file_sections = [
            'persona', 'prompts', 'guardrails', 'behaviors',
            'workflows', 'templates', 'command_templates', 'prd'
        ]

        for section in file_sections:
            if section in self.config_data:
                section_files = self.config_data[section]
                if isinstance(section_files, list):
                    for file_ref in section_files:
                        if isinstance(file_ref, str):
                            if not self._validate_single_file_reference(section, file_ref):
                                success = False

        if success:
            print("  ✅ File references valid")

        return success

    def _validate_single_file_reference(self, section: str, file_ref: str) -> bool:
        """Validate a single file reference."""
        # Handle relative paths from agent-config directory
        if not file_ref.startswith('/'):
            full_path = self.agent_config_dir / file_ref
        else:
            full_path = Path(file_ref)

        self.file_references[section].add(str(full_path))

        if not full_path.exists():
            self.errors.append(ValidationError(
                'error', 'missing_file',
                f"Referenced file not found in {section}: {file_ref}",
                file_path=file_ref,
                fix_suggestion=f"Create file or fix reference: {full_path}"
            ))
            return False

        if not full_path.is_file():
            self.errors.append(ValidationError(
                'error', 'not_file',
                f"Referenced path is not a file in {section}: {file_ref}",
                file_path=file_ref
            ))
            return False

        # Check file is readable
        try:
            with open(full_path, 'r') as f:
                f.read(1)  # Try to read at least one character
        except Exception as e:
            self.errors.append(ValidationError(
                'error', 'file_unreadable',
                f"Cannot read referenced file in {section}: {file_ref} - {str(e)}",
                file_path=file_ref
            ))
            return False

        return True

    def _validate_component_files(self) -> bool:
        """Validate individual component files for proper format."""
        success = True

        for section, file_paths in self.file_references.items():
            for file_path in file_paths:
                if not self._validate_component_file_format(section, Path(file_path)):
                    success = False

        if success:
            print("  ✅ Component files format valid")

        return success

    def _validate_component_file_format(self, section: str, file_path: Path) -> bool:
        """Validate format of individual component file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Check for YAML frontmatter
            if content.startswith('---'):
                try:
                    # Extract and parse frontmatter
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])

                        if isinstance(frontmatter, dict):
                            # Validate required frontmatter fields
                            required_fields = ['id', 'category', 'priority', 'version']
                            for field in required_fields:
                                if field not in frontmatter:
                                    self.errors.append(ValidationError(
                                        'warning', 'missing_frontmatter',
                                        f"Missing {field} in frontmatter: {file_path.name}",
                                        file_path=str(file_path)
                                    ))

                            # Validate category matches section
                            if 'category' in frontmatter:
                                expected_category = section.rstrip('s')  # Remove plural
                                if frontmatter['category'] != expected_category:
                                    self.errors.append(ValidationError(
                                        'warning', 'category_mismatch',
                                        f"Category '{frontmatter['category']}' doesn't match section '{section}': {file_path.name}",
                                        file_path=str(file_path)
                                    ))

                            # Store priority for validation
                            if 'priority' in frontmatter and 'id' in frontmatter:
                                self.priority_map[frontmatter['id']] = frontmatter['priority']

                except yaml.YAMLError as e:
                    self.errors.append(ValidationError(
                        'error', 'frontmatter_syntax',
                        f"Invalid YAML frontmatter in {file_path.name}: {str(e)}",
                        file_path=str(file_path)
                    ))
                    return False
            else:
                self.errors.append(ValidationError(
                    'info', 'no_frontmatter',
                    f"File missing YAML frontmatter: {file_path.name}",
                    file_path=str(file_path),
                    fix_suggestion="Add YAML frontmatter with id, category, priority, version"
                ))

        except Exception as e:
            self.errors.append(ValidationError(
                'error', 'file_validation',
                f"Error validating component file {file_path.name}: {str(e)}",
                file_path=str(file_path)
            ))
            return False

        return True

    def _validate_priorities(self) -> bool:
        """Validate priority assignments for conflicts and consistency."""
        if not self.priority_map:
            self.errors.append(ValidationError(
                'warning', 'no_priorities',
                "No priority information found in component files"
            ))
            return True

        # Check for priority conflicts (same priority in same category)
        category_priorities = defaultdict(list)

        for file_path in self.file_references:
            for path_str in self.file_references[file_path]:
                path = Path(path_str)
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            frontmatter = yaml.safe_load(parts[1])
                            if isinstance(frontmatter, dict) and 'priority' in frontmatter and 'category' in frontmatter:
                                category_priorities[frontmatter['category']].append({
                                    'priority': frontmatter['priority'],
                                    'id': frontmatter.get('id', path.name),
                                    'file': path.name
                                })
                except:
                    continue

        # Check for duplicate priorities within categories
        for category, items in category_priorities.items():
            priority_counts = defaultdict(list)
            for item in items:
                priority_counts[item['priority']].append(item)

            for priority, conflicting_items in priority_counts.items():
                if len(conflicting_items) > 1:
                    file_list = [item['file'] for item in conflicting_items]
                    self.errors.append(ValidationError(
                        'warning', 'priority_conflict',
                        f"Priority {priority} used by multiple {category} files: {', '.join(file_list)}",
                        fix_suggestion="Assign unique priorities within each category"
                    ))

        print("  ✅ Priority validation complete")
        return True

    def _validate_dependencies(self) -> bool:
        """Check for circular dependencies and missing dependencies."""
        # This is a simplified dependency check
        # In a full implementation, you'd parse actual dependencies from files

        dependencies = {}

        # Extract dependency information from files (simplified)
        for section, file_paths in self.file_references.items():
            for file_path_str in file_paths:
                file_path = Path(file_path_str)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()

                    # Look for dependency patterns (this is simplified)
                    deps = []
                    if 'depends_on:' in content:
                        # Extract dependencies (simplified regex)
                        dep_matches = re.findall(r'depends_on:\s*(.+)', content)
                        for match in dep_matches:
                            deps.extend([d.strip() for d in match.split(',')])

                    if deps:
                        dependencies[file_path.stem] = deps

                except:
                    continue

        # Check for circular dependencies using DFS
        def has_cycle(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in dependencies.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        visited = set()
        for node in dependencies:
            if node not in visited:
                if has_cycle(node, visited, set()):
                    self.errors.append(ValidationError(
                        'error', 'circular_dependency',
                        f"Circular dependency detected involving: {node}",
                        fix_suggestion="Review and resolve circular dependencies"
                    ))
                    return False

        print("  ✅ Dependency validation complete")
        return True

    def _validate_best_practices(self):
        """Check for best practice violations."""
        if not self.config_data:
            return

        # Check for version information
        if 'system' not in self.config_data or 'version' not in self.config_data.get('system', {}):
            self.errors.append(ValidationError(
                'info', 'best_practice',
                "Consider adding version information in system.version",
                fix_suggestion="Add version field to system configuration"
            ))

        # Check for quality gates configuration
        if 'quality_gates' not in self.config_data:
            self.errors.append(ValidationError(
                'info', 'best_practice',
                "Consider adding quality_gates configuration for automated validation",
                fix_suggestion="Add quality_gates section with validation rules"
            ))

        # Check for monitoring configuration
        if 'monitoring' not in self.config_data:
            self.errors.append(ValidationError(
                'info', 'best_practice',
                "Consider adding monitoring configuration for operational visibility",
                fix_suggestion="Add monitoring section with metrics and logging config"
            ))

    def _has_critical_errors(self) -> bool:
        """Check if there are any critical errors."""
        return any(error.severity == 'critical' for error in self.errors)

    def auto_fix_issues(self) -> int:
        """Attempt to automatically fix common issues."""
        fixed_count = 0

        print("🔧 Attempting automatic fixes...")

        # Create missing directories
        for error in self.errors:
            if error.category == 'missing_directory' and error.fix_suggestion:
                try:
                    # Extract directory path from fix suggestion
                    if 'mkdir -p' in error.fix_suggestion:
                        dir_path = error.fix_suggestion.split('mkdir -p ')[1]
                        Path(dir_path).mkdir(parents=True, exist_ok=True)
                        print(f"  ✅ Created directory: {dir_path}")
                        fixed_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to create directory: {str(e)}")

        # You could add more auto-fix logic here

        if fixed_count > 0:
            print(f"  🎉 Fixed {fixed_count} issues automatically")

        return fixed_count

    def generate_report(self, detailed: bool = False) -> Dict:
        """Generate validation report."""
        error_counts = defaultdict(int)
        for error in self.errors:
            error_counts[error.severity] += 1

        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_errors': len(self.errors),
                'critical': error_counts['critical'],
                'errors': error_counts['error'],
                'warnings': error_counts['warning'],
                'info': error_counts['info']
            },
            'validation_passed': not self._has_critical_errors() and error_counts['error'] == 0,
            'config_file': str(self.config_file),
            'claude_code_root': str(self.root)
        }

        if detailed:
            report['errors'] = [error.to_dict() for error in self.errors]
            report['file_references'] = {k: list(v) for k, v in self.file_references.items()}
            report['priority_map'] = self.priority_map

        return report

    def print_summary(self):
        """Print validation summary to console."""
        error_counts = defaultdict(int)
        for error in self.errors:
            error_counts[error.severity] += 1

        print("\n" + "="*60)
        print("📊 VALIDATION SUMMARY")
        print("="*60)

        if not self.errors:
            print("🎉 All validations passed! Configuration is healthy.")
            return

        print(f"Total issues found: {len(self.errors)}")
        if error_counts['critical']:
            print(f"  ❌ Critical: {error_counts['critical']}")
        if error_counts['error']:
            print(f"  🔴 Errors: {error_counts['error']}")
        if error_counts['warning']:
            print(f"  ⚠️  Warnings: {error_counts['warning']}")
        if error_counts['info']:
            print(f"  ℹ️  Info: {error_counts['info']}")

        # Print errors by category
        print("\n📋 ISSUES BY CATEGORY:")
        categories = defaultdict(list)
        for error in self.errors:
            categories[error.category].append(error)

        for category, errors in categories.items():
            print(f"\n{category.upper()}:")
            for error in errors[:5]:  # Limit to first 5 per category
                icon = {'critical': '❌', 'error': '🔴', 'warning': '⚠️', 'info': 'ℹ️'}[error.severity]
                print(f"  {icon} {error.message}")
                if error.fix_suggestion:
                    print(f"     💡 Fix: {error.fix_suggestion}")

            if len(errors) > 5:
                print(f"     ... and {len(errors) - 5} more")

        # Overall status
        print("\n🎯 OVERALL STATUS:")
        if self._has_critical_errors():
            print("❌ CRITICAL ISSUES FOUND - System may not function properly")
        elif error_counts['error'] > 0:
            print("🔴 ERRORS FOUND - Some features may not work correctly")
        elif error_counts['warning'] > 0:
            print("⚠️  WARNINGS FOUND - System functional but improvements recommended")
        else:
            print("✅ NO MAJOR ISSUES - Only informational items found")


def main():
    """Main entry point for configuration validation."""
    parser = argparse.ArgumentParser(
        description="Validate ClaudeCode configuration integrity"
    )
    parser.add_argument("--fix-auto", action="store_true",
                       help="Attempt to automatically fix common issues")
    parser.add_argument("--detailed", action="store_true",
                       help="Show detailed validation information")
    parser.add_argument("--export-report",
                       help="Export validation report to JSON file")
    parser.add_argument("--claude-code-root",
                       help="Path to ClaudeCode root directory",
                       default=".")

    args = parser.parse_args()

    # Initialize validator
    claude_code_root = Path(args.claude_code_root).resolve()
    validator = ConfigValidator(claude_code_root)

    # Run validation
    success = validator.validate_all()

    # Auto-fix if requested
    if args.fix_auto:
        fixed_count = validator.auto_fix_issues()
        if fixed_count > 0:
            print("\n🔄 Re-running validation after fixes...")
            validator = ConfigValidator(claude_code_root)
            success = validator.validate_all()

    # Print summary
    validator.print_summary()

    # Export report if requested
    if args.export_report:
        report = validator.generate_report(detailed=args.detailed)
        with open(args.export_report, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Report exported to: {args.export_report}")

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
