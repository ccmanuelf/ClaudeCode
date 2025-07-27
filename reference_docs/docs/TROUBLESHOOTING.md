# ClaudeCode Troubleshooting Guide

## Overview

This guide helps you diagnose and resolve common issues with ClaudeCode. Issues are organized by category with step-by-step solutions, from basic fixes to advanced recovery procedures.

## Table of Contents

1. [Quick Diagnostic Commands](#quick-diagnostic-commands)
2. [Configuration Issues](#configuration-issues)
3. [Progress State Problems](#progress-state-problems)
4. [Session Management Issues](#session-management-issues)
5. [Checkpoint and Recovery Problems](#checkpoint-and-recovery-problems)
6. [Performance Issues](#performance-issues)
7. [Integration Problems](#integration-problems)
8. [File System Issues](#file-system-issues)
9. [Emergency Recovery Procedures](#emergency-recovery-procedures)
10. [Getting Help](#getting-help)

---

## Quick Diagnostic Commands

Before diving into specific issues, run these commands to get a quick health check:

```bash
# 1. Configuration validation (most common issues)
python validate_config.py

# 2. System status check
python resume.py --debug

# 3. Check recent logs
tail -n 50 progress-state/config_validation.log

# 4. Verify file permissions
ls -la config.yaml progress-state/

# 5. Python environment check
python --version
python -c "import yaml, json; print('Dependencies OK')"
```

---

## Configuration Issues

### Issue 1: Configuration Validation Fails

**Symptoms:**
- ❌ Configuration validation failed
- Red error messages in `python validate_config.py`
- ClaudeCode won't start

**Quick Fix:**
```bash
# Run detailed validation
python validate_config.py --format text

# Common fixes:
# Fix YAML syntax
python -c "import yaml; yaml.safe_load(open('config.yaml'))" 

# Check file encoding
file config.yaml
```

**Detailed Solutions:**

#### YAML Syntax Errors
```bash
# Symptoms: "Invalid YAML syntax" error
# Solution 1: Check indentation (spaces only, no tabs)
cat -A config.yaml | head -20  # Shows tabs as ^I

# Solution 2: Validate YAML structure
python -c "
import yaml
try:
    with open('config.yaml') as f:
        yaml.safe_load(f)
    print('✅ YAML syntax is valid')
except yaml.YAMLError as e:
    print(f'❌ YAML Error: {e}')
"

# Solution 3: Common YAML fixes
# - Replace tabs with spaces
# - Add quotes around strings with special characters
# - Check list formatting (- item vs -item)
# - Ensure proper nesting
```

#### Missing File References
```bash
# Symptoms: "Referenced file not found" warnings
# Solution: Check which files are missing
python validate_config.py | grep "missing"

# Create missing directories
mkdir -p agent-config/{persona,prompts,guardrails,behaviors,workflows,templates,command_templates}

# Copy basic templates if needed
cp examples/configurations/basic_project_setup.yaml config.yaml
```

#### Permission Problems
```bash
# Symptoms: "Cannot read config file" or permission denied
# Solution: Fix file permissions
chmod 644 config.yaml
chmod -R 644 agent-config/
chmod 755 scripts/
```

### Issue 2: Invalid Configuration Values

**Symptoms:**
- Configuration loads but contains invalid values
- Unexpected behavior in ClaudeCode

**Solutions:**
```bash
# Check system section
python -c "
import yaml
config = yaml.safe_load(open('config.yaml'))
system = config.get('system', {})
print('Mode:', system.get('mode', 'MISSING'))
print('Version:', system.get('version', 'MISSING'))
"

# Valid modes: lite, standard, pro
# Valid versions: semantic versioning (e.g., "2.0")

# Fix invalid mode
sed -i 's/mode: .*/mode: "standard"/' config.yaml

# Fix missing version
sed -i '/^system:/,/^[^ ]/ s/version: .*/version: "2.0"/' config.yaml
```

---

## Progress State Problems

### Issue 3: Progress State Corruption

**Symptoms:**
- Progress percentages don't make sense
- Session resume shows incorrect information
- Checkpoint creation fails with state errors

**Diagnosis:**
```bash
# Check progress state file integrity
python -c "
import json
try:
    with open('progress-state/PROGRESS_STATE.json') as f:
        data = json.load(f)
    print('✅ Progress state JSON is valid')
    print(f'Current task: {data.get(\"current_session\", {}).get(\"active_task\", \"UNKNOWN\")}')
except json.JSONDecodeError as e:
    print(f'❌ JSON Error: {e}')
    print('Progress state file is corrupted')
except FileNotFoundError:
    print('❌ Progress state file missing')
"
```

**Solutions:**

#### Minor Corruption (JSON valid but data inconsistent)
```bash
# Repair progress state automatically
python scripts/progress_repair.py --auto-fix

# Manual verification
python validate_config.py
```

#### Major Corruption (Invalid JSON)
```bash
# Emergency recovery
python scripts/checkpoint_recovery.py emergency_recovery

# Alternative: Restore from backup
cp progress-state/backups/PROGRESS_STATE_backup_*.json progress-state/PROGRESS_STATE.json

# Last resort: Rebuild from scratch
python scripts/progress_rebuild.py --initialize
```

### Issue 4: Progress State File Missing

**Symptoms:**
- `FileNotFoundError: progress-state/PROGRESS_STATE.json`
- Fresh start behavior every time

**Solution:**
```bash
# Check if directory exists
ls -la progress-state/

# Recreate directory if missing
mkdir -p progress-state

# Initialize new progress state
python scripts/progress_rebuild.py --initialize

# Verify creation
ls -la progress-state/PROGRESS_STATE.json
```

---

## Session Management Issues

### Issue 5: Cannot Start Session

**Symptoms:**
- `python resume.py` fails to start
- Import errors or module not found

**Solutions:**

#### Python Path Issues
```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Add current directory to path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run with explicit path
PYTHONPATH=. python resume.py
```

#### Missing Dependencies
```bash
# Check for required modules
# Check if your AI CLI tool is properly installed and accessible
which claude-cli  # or your specific AI tool
# OR
gemini --version
# OR  
opencode --help

# Verify ClaudeCode framework activation
# Use SESSION_INITIALIZATION.md prompt with your AI tool
```

#### Script Permissions
```bash
# Check script permissions
ls -la resume.py scripts/

# Fix permissions
chmod +x resume.py
chmod +x scripts/*.py
```

### Issue 6: Session Context Lost

**Symptoms:**
- Session starts but shows no previous work
- "Starting fresh" despite previous sessions

**Solutions:**
```bash
# Check session state
python -c "
import json
try:
    with open('progress-state/PROGRESS_STATE.json') as f:
        data = json.load(f)
    session = data.get('current_session', {})
    print(f'Session ID: {session.get(\"session_id\", \"MISSING\")}')
    print(f'Last Activity: {session.get(\"last_activity\", \"MISSING\")}')
    print(f'Active Task: {session.get(\"active_task\", \"MISSING\")}')
except Exception as e:
    print(f'❌ Cannot read session state: {e}')
"

# Rebuild session context
python scripts/session_recovery.py --rebuild-context

# Force context restoration
python resume.py --force-context-rebuild
```

---

## Checkpoint and Recovery Problems

### Issue 7: Checkpoint Creation Fails

**Symptoms:**
- "Failed to create checkpoint" errors
- Checkpoint option in menu doesn't work

**Diagnosis:**
```bash
# Check checkpoint directory
ls -la progress-state/checkpoints/

# Check disk space
df -h .

# Check write permissions
touch progress-state/checkpoints/test_write
rm progress-state/checkpoints/test_write
```

**Solutions:**
```bash
# Create missing checkpoint directory
mkdir -p progress-state/checkpoints

# Fix permissions
chmod 755 progress-state/checkpoints

# Clean up old checkpoints if disk space is low
python scripts/checkpoint_cleanup.py --older-than 7days

# Manual checkpoint creation test
python -c "
import json
from datetime import datetime
checkpoint = {
    'checkpoint_id': 'TEST001',
    'timestamp': datetime.now().isoformat(),
    'description': 'Test checkpoint'
}
with open('progress-state/checkpoints/test_checkpoint.json', 'w') as f:
    json.dump(checkpoint, f, indent=2)
print('✅ Manual checkpoint created successfully')
"
```

### Issue 8: Recovery Fails

**Symptoms:**
- "Recovery failed" messages
- Cannot restore from checkpoint

**Solutions:**

#### Validate Checkpoint First
```bash
# List available checkpoints
python scripts/checkpoint_recovery.py list

# Validate specific checkpoint
python scripts/checkpoint_recovery.py validate CP012

# Check validation results
python scripts/checkpoint_recovery.py validate CP012 --verbose
```

#### Emergency Recovery Process
```bash
# Try emergency recovery (uses most recent valid checkpoint)
python scripts/checkpoint_recovery.py emergency_recovery

# If that fails, use emergency rebuild
python scripts/checkpoint_recovery.py emergency_rebuild --from-git-history

# Last resort: clean slate
python scripts/progress_rebuild.py --clean-slate
```

---

## Performance Issues

### Issue 9: Slow Startup

**Symptoms:**
- ClaudeCode takes > 30 seconds to start
- Long delays during configuration validation

**Solutions:**

#### Profile Startup Performance
```bash
# Time configuration validation
time python validate_config.py

# Profile with detailed timing
python -c "
import time
start = time.time()
import yaml
mid1 = time.time()
with open('config.yaml') as f:
    config = yaml.safe_load(f)
mid2 = time.time()
print(f'Import time: {mid1-start:.2f}s')
print(f'Config load time: {mid2-mid1:.2f}s')
print(f'Total time: {mid2-start:.2f}s')
"
```

#### Optimize Configuration
```bash
# Reduce config file size (remove unused sections)
cp config.yaml config.yaml.backup
python scripts/config_optimizer.py --remove-unused

# Clean up old files
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Optimize checkpoint storage
python scripts/checkpoint_cleanup.py --compress
```

### Issue 10: High Memory Usage

**Symptoms:**
- System becomes unresponsive
- Out of memory errors

**Solutions:**
```bash
# Monitor memory usage
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"

# Reduce memory usage
# 1. Limit checkpoint retention
echo "
progress_state:
  max_checkpoints: 20  # Reduce from default 50
  checkpoint_frequency: 60  # Increase from 30 minutes
" >> config.yaml

# 2. Disable verbose logging
sed -i 's/detailed_logging: true/detailed_logging: false/' config.yaml

# 3. Clear old session data
python scripts/session_cleanup.py --older-than 7days
```

---

## Integration Problems

### Issue 11: GitHub Integration Fails

**Symptoms:**
- GitHub features not working
- API authentication errors

**Solutions:**
```bash
# Check GitHub configuration
python -c "
import yaml
config = yaml.safe_load(open('config.yaml'))
github = config.get('integrations', {}).get('github', {})
print(f'GitHub enabled: {github.get(\"enabled\", False)}')
print(f'Repository: {github.get(\"repository_pattern\", \"MISSING\")}')
"

# Test GitHub connectivity (if enabled)
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/user

# Fix common GitHub issues
# 1. Enable GitHub integration
sed -i 's/github:/github:\n    enabled: true/' config.yaml

# 2. Set repository pattern
sed -i 's/repository_pattern: .*/repository_pattern: "your-org\/your-repo"/' config.yaml
```

### Issue 12: CI/CD Integration Problems

**Symptoms:**
- Pipeline failures
- Configuration not recognized in CI

**Solutions:**
```bash
# Check CI environment
echo "Environment variables:"
env | grep -E "(CI|GITHUB|GITLAB|JENKINS)"

# Create CI-specific config
cp config.yaml config.ci.yaml
sed -i 's/mode: "pro"/mode: "lite"/' config.ci.yaml
sed -i 's/detailed_logging: true/detailed_logging: false/' config.ci.yaml

# Test in CI mode
CLAUDECODE_CONFIG=config.ci.yaml python validate_config.py
```

---

## File System Issues

### Issue 13: Permission Denied Errors

**Symptoms:**
- Cannot read/write files
- Permission denied on script execution

**Solutions:**
```bash
# Check current permissions
ls -la config.yaml
ls -la scripts/
ls -la progress-state/

# Fix common permission issues
chmod 644 config.yaml
chmod 755 scripts/*.py
chmod 755 progress-state/
chmod 644 progress-state/*.json
chmod 644 progress-state/*.md

# Fix ownership if needed (Linux/Mac)
chown $USER:$USER -R .
```

### Issue 14: Disk Space Issues

**Symptoms:**
- "No space left on device" errors
- Checkpoint creation fails

**Solutions:**
```bash
# Check disk space
df -h .

# Find large files in ClaudeCode
du -h . | sort -hr | head -20

# Clean up automatically
python scripts/cleanup.py --aggressive

# Manual cleanup
rm -rf progress-state/checkpoints/*_backup_*
find . -name "*.log" -mtime +7 -delete
find . -name "*.tmp" -delete
```

---

## Emergency Recovery Procedures

### Emergency 1: Complete System Recovery

**When to use:** ClaudeCode completely broken, nothing works

**Recovery Steps:**
```bash
# Step 1: Backup current state
mkdir -p emergency_backup
cp -r progress-state/ emergency_backup/ 2>/dev/null || true
cp config.yaml emergency_backup/ 2>/dev/null || true

# Step 2: Reset to known good state
python scripts/emergency_reset.py --create-backup

# Step 3: Reinitialize with basic config
cp examples/configurations/basic_project_setup.yaml config.yaml

# Step 4: Test basic functionality
python validate_config.py

# Step 5: Restore data if possible
python scripts/emergency_restore.py --from-backup emergency_backup/

# Step 6: Verify recovery
python resume.py --test-mode
```

### Emergency 2: Data Recovery

**When to use:** Progress state lost but files exist

**Recovery Steps:**
```bash
# Step 1: Attempt automatic recovery
python scripts/data_recovery.py --scan-filesystem

# Step 2: Recover from git history
python scripts/data_recovery.py --from-git-history

# Step 3: Manual state reconstruction
python scripts/manual_recovery.py --interactive

# Step 4: Validate recovered data
python validate_config.py
python scripts/checkpoint_recovery.py validate_all
```

### Emergency 3: Clean Slate Recovery

**When to use:** Nothing else works, start fresh but preserve project files

**Recovery Steps:**
```bash
# Step 1: Preserve project files
mkdir -p recovery_preserve
cp -r src/ recovery_preserve/ 2>/dev/null || true
cp -r docs/ recovery_preserve/ 2>/dev/null || true
cp -r tests/ recovery_preserve/ 2>/dev/null || true

# Step 2: Complete reset
rm -rf progress-state/ config.yaml

# Step 3: Reinitialize
cp examples/configurations/basic_project_setup.yaml config.yaml
python scripts/progress_rebuild.py --initialize

# Step 4: Restore project files
cp -r recovery_preserve/* . 2>/dev/null || true

# Step 5: Create initial checkpoint
python resume.py
# Choose option 2: Create checkpoint
# Description: "Emergency recovery - clean slate initialization"
```

---

## Advanced Troubleshooting

### Debug Mode

Enable debug mode for detailed diagnostics:
```bash
# Enable debug in config.yaml
echo "
debug:
  enabled: true
  verbose_logging: true
  trace_operations: true
" >> config.yaml

# Run with debug output
python resume.py --debug 2>&1 | tee debug.log
```

### Log Analysis

```bash
# View recent logs
tail -f progress-state/config_validation.log

# Search for errors
grep -i error progress-state/*.log

# Analyze patterns
awk '{print $1, $2}' progress-state/config_validation.log | sort | uniq -c
```

### System Health Check

```bash
# Comprehensive health check
python scripts/health_check.py --comprehensive

# Generate diagnostic report
python scripts/diagnostic_report.py --output health_report.txt
```

---

## Getting Help

### Before Seeking Help

1. Run diagnostic commands from this guide
2. Check the error logs
3. Try the suggested solutions for your issue
4. Document what you tried and the results

### Information to Provide

When seeking help, include:
```bash
# System information
echo "OS: $(uname -a)"
echo "Python: $(python --version)"
echo "ClaudeCode: $(grep version config.yaml)"

# Error details
python validate_config.py 2>&1
tail -20 progress-state/config_validation.log

# Configuration summary
python -c "
import yaml
config = yaml.safe_load(open('config.yaml'))
print(f'Mode: {config.get(\"system\", {}).get(\"mode\", \"UNKNOWN\")}')
print(f'Progress tracking: {config.get(\"progress_state\", {}).get(\"enabled\", False)}')
"
```

### Self-Help Resources

1. **Configuration Reference**: Check `docs/CONFIGURATION_VALIDATION.md`
2. **Usage Examples**: Review `docs/USAGE_EXAMPLES.md`
3. **Best Practices**: See `docs/BEST_PRACTICES.md`
4. **Quick Start**: Reference `docs/QUICK_START.md`

### Emergency Contacts

If all else fails:
1. Create emergency backup: `cp -r . ../claudecode_emergency_backup`
2. Document the issue with logs and error messages
3. Try emergency recovery procedures above
4. Reach out to ClaudeCode support with diagnostic information

---

## Prevention Tips

### Regular Maintenance
```bash
# Weekly maintenance script
#!/bin/bash
echo "🔧 ClaudeCode Weekly Maintenance"
python validate_config.py
python scripts/checkpoint_cleanup.py --older-than 30days
python scripts/health_check.py
echo "✅ Maintenance complete"
```

### Backup Strategy
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
mkdir -p backups
cp config.yaml backups/config_$DATE.yaml
cp -r progress-state/ backups/progress_state_$DATE/
echo "✅ Backup complete: $DATE"
```

### Monitoring
```bash
# Set up monitoring
echo "*/15 * * * * cd /path/to/claudecode && python scripts/health_monitor.py --alert-on-issues" | crontab -
```

---

**Remember**: Most ClaudeCode issues are configuration-related and can be resolved quickly with the diagnostic commands and solutions in this guide. When in doubt, start with `python validate_config.py` and work through the suggestions systematically.