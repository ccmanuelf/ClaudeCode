#!/usr/bin/env python3
"""
ClaudeCode Configuration Validator
Provides comprehensive validation for the ClaudeCode configuration system.

ABOUTME: This script validates the config.yaml file on system startup and provides
detailed reporting on configuration issues, missing files, and recommendations.
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('progress-state/config_validation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Validation issue severity levels."""
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    """Represents a single validation issue."""
    severity: ValidationSeverity
    section: str
    message: str
    suggestion: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class ValidationReport:
    """Complete validation report."""
    config_file: str
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    file_checks: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    summary: Dict[str, int] = field(default_factory=dict)

    def calculate_summary(self):
        """Calculate summary statistics."""
        self.summary = {
            'critical': len([i for i in self.issues if i.severity == ValidationSeverity.CRITICAL]),
            'errors': len([i for i in self.issues if i.severity == ValidationSeverity.ERROR]),
            'warnings': len([i for i in self.issues if i.severity == ValidationSeverity.WARNING]),
            'info': len([i for i in self.issues if i.severity == ValidationSeverity.INFO]),
            'total_files_checked': len(self.file_checks),
            'missing_files': len([f for f, data in self.file_checks.items() if not data.get('exists', False)])
        }


class ConfigValidator:
    """Main configuration validation engine."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the validator."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.config_file = self.project_root / "config.yaml"
        self.config_data: Dict[str, Any] = {}

        # Required sections in config.yaml
        self.required_sections = {
            'persona': 'AI persona configuration',
            'prompts': 'Prompt engineering framework',
            'workflows': 'Development workflow engine',
            'system': 'System configuration',
            'progress_state': 'Progress state management'
        }

        # Optional but recommended sections
        self.recommended_sections = {
            'guardrails': 'Development guardrails and quality control',
            'behaviors': 'AI behavior and cognitive management',
            'templates': 'Template and code generation framework',
            'tasks': 'Dynamic task management',
            'features': 'Feature development tracking',
            'monitoring': 'Monitoring and analytics',
            'security': 'Security and compliance'
        }

    def validate_config(self) -> ValidationReport:
        """Perform comprehensive configuration validation."""
        report = ValidationReport(
            config_file=str(self.config_file),
            is_valid=True
        )

        try:
            # Step 1: Check if config file exists
            if not self.config_file.exists():
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.CRITICAL,
                    section="file_system",
                    message=f"Configuration file not found: {self.config_file}",
                    suggestion="Create config.yaml file in the project root directory"
                ))
                report.is_valid = False
                return report

            # Step 2: Validate YAML syntax
            self._validate_yaml_syntax(report)
            if not report.is_valid:
                return report

            # Step 3: Load configuration data
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config_data = yaml.safe_load(f)

            # Step 4: Validate structure
            self._validate_structure(report)

            # Step 5: Validate file references
            self._validate_file_references(report)

            # Step 6: Validate system configuration
            self._validate_system_config(report)

            # Step 7: Validate progress state configuration
            self._validate_progress_state(report)

            # Step 8: Validate integration settings
            self._validate_integrations(report)

            # Step 9: Check for best practices
            self._validate_best_practices(report)

        except Exception as e:
            report.issues.append(ValidationIssue(
                severity=ValidationSeverity.CRITICAL,
                section="validation_engine",
                message=f"Validation engine error: {str(e)}",
                suggestion="Check validator implementation and config file format"
            ))
            report.is_valid = False
            logger.error(f"Configuration validation failed: {e}")

        # Calculate summary statistics
        report.calculate_summary()

        # Determine overall validity
        critical_errors = [i for i in report.issues if i.severity == ValidationSeverity.CRITICAL]
        errors = [i for i in report.issues if i.severity == ValidationSeverity.ERROR]
        report.is_valid = len(critical_errors) == 0 and len(errors) == 0

        return report

    def _validate_yaml_syntax(self, report: ValidationReport) -> None:
        """Validate YAML syntax."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            report.issues.append(ValidationIssue(
                severity=ValidationSeverity.CRITICAL,
                section="yaml_syntax",
                message=f"Invalid YAML syntax: {str(e)}",
                suggestion="Fix YAML syntax errors using a YAML validator"
            ))
            report.is_valid = False
        except Exception as e:
            report.issues.append(ValidationIssue(
                severity=ValidationSeverity.CRITICAL,
                section="file_access",
                message=f"Cannot read config file: {str(e)}",
                suggestion="Check file permissions and encoding"
            ))
            report.is_valid = False

    def _validate_structure(self, report: ValidationReport) -> None:
        """Validate configuration structure."""
        if not isinstance(self.config_data, dict):
            report.issues.append(ValidationIssue(
                severity=ValidationSeverity.CRITICAL,
                section="structure",
                message="Configuration must be a YAML dictionary",
                suggestion="Ensure config.yaml contains key-value pairs at root level"
            ))
            return

        # Check required sections
        for section, description in self.required_sections.items():
            if section not in self.config_data:
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section=section,
                    message=f"Missing required section: {section}",
                    suggestion=f"Add {section} section for {description}"
                ))

        # Check recommended sections
        for section, description in self.recommended_sections.items():
            if section not in self.config_data:
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    section=section,
                    message=f"Missing recommended section: {section}",
                    suggestion=f"Consider adding {section} section for {description}"
                ))

    def _validate_file_references(self, report: ValidationReport) -> None:
        """Validate all file references in the configuration."""
        file_sections = ['persona', 'prompts', 'guardrails', 'behaviors', 'workflows', 'templates', 'command_templates']

        for section_name in file_sections:
            if section_name not in self.config_data:
                continue

            section_data = self.config_data[section_name]
            if isinstance(section_data, list):
                self._validate_file_list(section_data, section_name, report)
            elif isinstance(section_data, dict):
                self._validate_file_dict(section_data, section_name, report)

    def _validate_file_list(self, file_list: List[str], section: str, report: ValidationReport) -> None:
        """Validate a list of file references."""
        for file_path in file_list:
            if not isinstance(file_path, str):
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section=section,
                    message=f"Invalid file path format in {section}: {file_path}",
                    suggestion="File paths must be strings"
                ))
                continue

            full_path = self.project_root / file_path
            report.file_checks[file_path] = {
                'exists': full_path.exists(),
                'readable': full_path.exists() and os.access(full_path, os.R_OK),
                'size': full_path.stat().st_size if full_path.exists() else 0,
                'section': section
            }

            if not full_path.exists():
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    section=section,
                    message=f"Referenced file not found: {file_path}",
                    suggestion=f"Create the missing file or remove reference from {section}",
                    file_path=file_path
                ))

    def _validate_file_dict(self, file_dict: Dict[str, Any], section: str, report: ValidationReport) -> None:
        """Validate file references in dictionary format."""
        for key, value in file_dict.items():
            if isinstance(value, str) and (value.endswith('.md') or value.endswith('.json')):
                full_path = self.project_root / value
                report.file_checks[value] = {
                    'exists': full_path.exists(),
                    'readable': full_path.exists() and os.access(full_path, os.R_OK),
                    'size': full_path.stat().st_size if full_path.exists() else 0,
                    'section': section,
                    'key': key
                }

                if not full_path.exists():
                    report.issues.append(ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        section=section,
                        message=f"Referenced file not found: {value} (for {key})",
                        suggestion=f"Create the missing file or update reference in {section}.{key}",
                        file_path=value
                    ))

    def _validate_system_config(self, report: ValidationReport) -> None:
        """Validate system configuration section."""
        if 'system' not in self.config_data:
            return

        system_config = self.config_data['system']

        # Validate required system fields
        required_system_fields = ['version', 'mode']
        for field in required_system_fields:
            if field not in system_config:
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section="system",
                    message=f"Missing required system field: {field}",
                    suggestion=f"Add {field} to system configuration"
                ))

        # Validate mode values
        if 'mode' in system_config:
            valid_modes = ['lite', 'standard', 'pro']
            if system_config['mode'] not in valid_modes:
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section="system",
                    message=f"Invalid mode: {system_config['mode']}",
                    suggestion=f"Mode must be one of: {', '.join(valid_modes)}"
                ))

    def _validate_progress_state(self, report: ValidationReport) -> None:
        """Validate progress state configuration."""
        if 'progress_state' not in self.config_data:
            return

        progress_config = self.config_data['progress_state']

        # Check state file reference
        if 'state_file' in progress_config:
            state_file_path = self.project_root / progress_config['state_file']
            report.file_checks[progress_config['state_file']] = {
                'exists': state_file_path.exists(),
                'readable': state_file_path.exists() and os.access(state_file_path, os.R_OK),
                'size': state_file_path.stat().st_size if state_file_path.exists() else 0,
                'section': 'progress_state'
            }

            if not state_file_path.exists():
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    section="progress_state",
                    message=f"Progress state file not found: {progress_config['state_file']}",
                    suggestion="This file will be created automatically on first run"
                ))

        # Validate checkpoint frequency
        if 'checkpoint_frequency' in progress_config:
            freq = progress_config['checkpoint_frequency']
            if not isinstance(freq, int) or freq < 1:
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section="progress_state",
                    message=f"Invalid checkpoint frequency: {freq}",
                    suggestion="Checkpoint frequency must be a positive integer (minutes)"
                ))

    def _validate_integrations(self, report: ValidationReport) -> None:
        """Validate integration configurations."""
        if 'integrations' not in self.config_data:
            return

        integrations = self.config_data['integrations']

        # Validate GitHub integration
        if 'github' in integrations:
            github_config = integrations['github']
            if github_config.get('enabled', False):
                if 'repository_pattern' not in github_config:
                    report.issues.append(ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        section="integrations.github",
                        message="GitHub integration enabled but no repository pattern specified",
                        suggestion="Add repository_pattern field for GitHub integration"
                    ))

    def _validate_best_practices(self, report: ValidationReport) -> None:
        """Check configuration against best practices."""
        # Check if monitoring is enabled
        if 'monitoring' in self.config_data:
            monitoring = self.config_data['monitoring']
            if not monitoring.get('session_tracking', False):
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    section="monitoring",
                    message="Session tracking is disabled",
                    suggestion="Enable session tracking for better development insights"
                ))

        # Check security settings
        if 'security' in self.config_data:
            security = self.config_data['security']
            if not security.get('api_key_protection', False):
                report.issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    section="security",
                    message="API key protection is disabled",
                    suggestion="Enable API key protection for security"
                ))

    def generate_report(self, report: ValidationReport, format: str = "text") -> str:
        """Generate a formatted validation report."""
        if format == "json":
            return self._generate_json_report(report)
        else:
            return self._generate_text_report(report)

    def _generate_text_report(self, report: ValidationReport) -> str:
        """Generate a text-formatted validation report."""
        lines = []
        lines.append("=" * 80)
        lines.append("🔍 CLAUDECODE CONFIGURATION VALIDATION REPORT")
        lines.append("=" * 80)
        lines.append(f"📁 Config File: {report.config_file}")
        status = "YES" if report.is_valid else "NO"
        if report.is_valid and report.summary['warnings'] > 0:
            status += " (with warnings)"
        lines.append(f"✅ Valid: {status}")
        lines.append("")

        # Summary
        lines.append("📊 SUMMARY")
        lines.append("-" * 40)
        lines.append(f"Critical Issues: {report.summary['critical']}")
        lines.append(f"Errors: {report.summary['errors']}")
        lines.append(f"Warnings: {report.summary['warnings']}")
        lines.append(f"Info Items: {report.summary['info']}")
        lines.append(f"Files Checked: {report.summary['total_files_checked']}")
        lines.append(f"Missing Files: {report.summary['missing_files']}")
        lines.append("")

        # Issues
        if report.issues:
            lines.append("🚨 ISSUES FOUND")
            lines.append("-" * 40)
            for issue in sorted(report.issues, key=lambda x: x.severity.value):
                severity_icon = {
                    ValidationSeverity.CRITICAL: "🔴",
                    ValidationSeverity.ERROR: "🟠",
                    ValidationSeverity.WARNING: "🟡",
                    ValidationSeverity.INFO: "🔵"
                }[issue.severity]

                lines.append(f"{severity_icon} {issue.severity.value}: {issue.message}")
                lines.append(f"   Section: {issue.section}")
                if issue.suggestion:
                    lines.append(f"   💡 Suggestion: {issue.suggestion}")
                if issue.file_path:
                    lines.append(f"   📄 File: {issue.file_path}")
                lines.append("")

        # File checks summary
        if report.file_checks:
            lines.append("📁 FILE REFERENCE CHECKS")
            lines.append("-" * 40)
            for file_path, check_result in report.file_checks.items():
                status = "✅" if check_result['exists'] else "❌"
                size = f"({check_result['size']} bytes)" if check_result['exists'] else "(missing)"
                lines.append(f"{status} {file_path} {size}")
            lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)

    def _generate_json_report(self, report: ValidationReport) -> str:
        """Generate a JSON-formatted validation report."""
        report_data = {
            'config_file': report.config_file,
            'is_valid': report.is_valid,
            'summary': report.summary,
            'issues': [
                {
                    'severity': issue.severity.value,
                    'section': issue.section,
                    'message': issue.message,
                    'suggestion': issue.suggestion,
                    'file_path': issue.file_path,
                    'line_number': issue.line_number
                }
                for issue in report.issues
            ],
            'file_checks': report.file_checks
        }
        return json.dumps(report_data, indent=2)

    def validate_and_report(self, format: str = "text", output_file: Optional[str] = None) -> Tuple[bool, str]:
        """Validate configuration and generate report."""
        report = self.validate_config()
        report_text = self.generate_report(report, format)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)

        return report.is_valid, report_text


def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description="ClaudeCode Configuration Validator")
    parser.add_argument("--config", help="Path to config.yaml file")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")

    args = parser.parse_args()

    project_root = Path(args.config).parent if args.config else Path.cwd()
    validator = ConfigValidator(project_root)

    if args.config:
        validator.config_file = Path(args.config)

    is_valid, report = validator.validate_and_report(args.format, args.output)

    if not args.quiet:
        print(report)

    # Exit with error code if validation failed
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
