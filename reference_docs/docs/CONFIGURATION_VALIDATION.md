# ClaudeCode Configuration Validation System

## Overview

The ClaudeCode Configuration Validation System provides comprehensive validation of the `config.yaml` file to ensure system integrity and proper setup. This system validates configuration syntax, file references, and best practices compliance.

## Features

### 🔍 **Validation Capabilities**
- **YAML Syntax Validation**: Ensures proper YAML formatting
- **File Reference Checking**: Verifies all referenced files exist
- **Structure Validation**: Confirms required sections are present
- **Best Practices Compliance**: Checks against recommended configurations
- **Detailed Reporting**: Provides actionable feedback and suggestions

### ⚡ **Integration Points**
- **Startup Validation**: Automatic validation when running `python resume.py`
- **Standalone Validation**: Direct validation via `python validate_config.py`
- **Menu Integration**: Available through interactive resume menu
- **Command Line Interface**: Full CLI support with multiple output formats

## Usage

### Quick Validation
```bash
# Validate configuration with text output
python validate_config.py

# Validate with JSON output
python scripts/config_validator.py --format json

# Save validation report to file
python scripts/config_validator.py --output validation_report.txt
```

### Integrated Validation
The validation system automatically runs when you start ClaudeCode:
```bash
python resume.py
```

During startup, you'll see:
```
🔍 VALIDATING CONFIGURATION...
------------------------------
✅ Configuration validation passed!
```

### Interactive Menu Access
When running `python resume.py`, choose option 8 to run configuration validation:
```
8. Validate configuration
```

## Validation Levels

### 🔴 **Critical Issues**
- Missing `config.yaml` file
- Invalid YAML syntax
- Corrupted configuration structure
- System cannot start with critical issues

### 🟠 **Errors**
- Missing required sections
- Invalid configuration values
- Broken dependencies
- System functionality may be impaired

### 🟡 **Warnings**
- Missing referenced files
- Missing recommended sections
- Suboptimal configurations
- System works but with reduced functionality

### 🔵 **Info Items**
- Best practice recommendations
- Performance optimizations
- Security suggestions
- Enhancement opportunities

## Configuration Sections Validated

### Required Sections
- `persona`: AI persona configuration
- `prompts`: Prompt engineering framework
- `workflows`: Development workflow engine
- `system`: System configuration
- `progress_state`: Progress state management

### Recommended Sections
- `guardrails`: Development guardrails and quality control
- `behaviors`: AI behavior and cognitive management
- `templates`: Template and code generation framework
- `tasks`: Dynamic task management
- `features`: Feature development tracking
- `monitoring`: Monitoring and analytics
- `security`: Security and compliance

## File Reference Validation

The validator checks all file references in these sections:
- `persona`: AI persona files
- `prompts`: Prompt framework files
- `guardrails`: Quality control files
- `behaviors`: Behavior management files
- `workflows`: Workflow definition files
- `templates`: Template files
- `command_templates`: Command template files

### File Check Results
- ✅ **Exists and Readable**: File found and accessible
- ❌ **Missing**: File referenced but not found
- 🔒 **Permission Issues**: File exists but not readable

## Validation Report Format

### Text Report Structure
```
================================================================================
🔍 CLAUDECODE CONFIGURATION VALIDATION REPORT
================================================================================
📁 Config File: /path/to/config.yaml
✅ Valid: YES (with warnings)

📊 SUMMARY
----------------------------------------
Critical Issues: 0
Errors: 0
Warnings: 39
Info Items: 0
Files Checked: 40
Missing Files: 39

🚨 ISSUES FOUND
----------------------------------------
🟡 WARNING: Referenced file not found: persona/professor_spark.md
   Section: persona
   💡 Suggestion: Create the missing file or remove reference from persona
   📄 File: persona/professor_spark.md

📁 FILE REFERENCE CHECKS
----------------------------------------
❌ persona/professor_spark.md (missing)
✅ progress-state/PROGRESS_STATE.json (18054 bytes)
================================================================================
```

### JSON Report Structure
```json
{
  "config_file": "/path/to/config.yaml",
  "is_valid": true,
  "summary": {
    "critical": 0,
    "errors": 0,
    "warnings": 39,
    "info": 0,
    "total_files_checked": 40,
    "missing_files": 39
  },
  "issues": [
    {
      "severity": "WARNING",
      "section": "persona",
      "message": "Referenced file not found: persona/professor_spark.md",
      "suggestion": "Create the missing file or remove reference from persona",
      "file_path": "persona/professor_spark.md",
      "line_number": null
    }
  ],
  "file_checks": {
    "persona/professor_spark.md": {
      "exists": false,
      "readable": false,
      "size": 0,
      "section": "persona"
    }
  }
}
```

## Command Line Interface

### Basic Usage
```bash
python scripts/config_validator.py [OPTIONS]
```

### Options
- `--config PATH`: Path to config.yaml file (default: ./config.yaml)
- `--format FORMAT`: Output format (text|json, default: text)
- `--output FILE`: Output file path (default: stdout)
- `--quiet`: Suppress console output

### Examples
```bash
# Validate specific config file
python scripts/config_validator.py --config /path/to/config.yaml

# Generate JSON report
python scripts/config_validator.py --format json --output report.json

# Quiet validation (exit code only)
python scripts/config_validator.py --quiet
echo $?  # 0 if valid, 1 if invalid
```

## Integration with ClaudeCode Systems

### Startup Integration
The validation system is integrated into the ClaudeCode startup sequence:

1. **Automatic Validation**: Runs when `python resume.py` is executed
2. **Interactive Prompts**: Allows continuation with warnings
3. **Error Blocking**: Prevents startup with critical errors
4. **Progress Tracking**: Logs validation results

### Checkpoint Integration
Configuration validation status is included in checkpoint data:
```json
{
  "validation_status": "VALID_WITH_WARNINGS",
  "config_validation": {
    "timestamp": "2024-12-17T10:30:00Z",
    "issues_count": 39,
    "critical_count": 0,
    "error_count": 0
  }
}
```

### Recovery Integration
The validation system supports recovery scenarios:
- **Config Corruption**: Detects and reports corrupted configurations
- **Missing Files**: Identifies files needed for recovery
- **Dependency Validation**: Ensures dependencies for recovery are met

## Best Practices

### Configuration Management
1. **Regular Validation**: Run validation after configuration changes
2. **Version Control**: Track configuration changes in git
3. **Backup Configs**: Maintain backup configurations
4. **Documentation**: Document custom configuration sections

### File Organization
1. **Consistent Paths**: Use relative paths from project root
2. **Directory Structure**: Maintain organized directory hierarchy
3. **File Naming**: Use descriptive, consistent file names
4. **Reference Hygiene**: Remove unused file references

### Error Resolution
1. **Critical First**: Address critical issues immediately
2. **Systematic Approach**: Work through errors by section
3. **Testing**: Validate after each fix
4. **Documentation**: Update documentation when fixing issues

## Troubleshooting

### Common Issues

#### YAML Syntax Errors
```
🔴 CRITICAL: Invalid YAML syntax: while parsing a flow sequence
```
**Solution**: Check YAML formatting, indentation, and special characters

#### Missing Required Sections
```
🟠 ERROR: Missing required section: system
```
**Solution**: Add the missing section to config.yaml

#### File Not Found
```
🟡 WARNING: Referenced file not found: persona/professor_spark.md
```
**Solution**: Create the missing file or remove the reference

#### Permission Issues
```
🟠 ERROR: Cannot read config file: Permission denied
```
**Solution**: Check file permissions and ownership

### Debug Mode
For detailed debugging, check the validation log:
```bash
tail -f progress-state/config_validation.log
```

### Recovery Procedures
1. **Backup Configuration**: Copy working config.yaml
2. **Reset to Default**: Use template configuration
3. **Incremental Validation**: Add sections one by one
4. **Professional Help**: Consult ClaudeCode documentation

## API Reference

### ConfigValidator Class
```python
from config_validator import ConfigValidator

# Initialize validator
validator = ConfigValidator(project_root="/path/to/project")

# Perform validation
report = validator.validate_config()

# Generate formatted report
text_report = validator.generate_report(report, format="text")
json_report = validator.generate_report(report, format="json")

# Validate and report in one call
is_valid, report_text = validator.validate_and_report(format="text")
```

### ValidationReport Structure
```python
@dataclass
class ValidationReport:
    config_file: str
    is_valid: bool
    issues: List[ValidationIssue]
    file_checks: Dict[str, Dict[str, Any]]
    summary: Dict[str, int]
```

### ValidationIssue Structure
```python
@dataclass
class ValidationIssue:
    severity: ValidationSeverity
    section: str
    message: str
    suggestion: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
```

## Version History

### Version 1.0.0 (2024-12-17)
- Initial release with comprehensive validation
- YAML syntax validation
- File reference checking
- Startup integration
- CLI interface
- JSON and text reporting
- Integration with ClaudeCode resume system

---

**Note**: This validation system is part of ClaudeCode P1.2.2 implementation and provides the foundation for reliable configuration management throughout the development lifecycle.