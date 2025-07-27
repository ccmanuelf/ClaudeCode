# Resume Commands Reference
**ClaudeCode Progress Continuity System**
Version: 1.0 | Last Updated: 2024-12-17

## 📋 COMMAND OVERVIEW

This document defines the standardized commands for resuming work, managing progress, and maintaining context continuity across sessions in the ClaudeCode development system.

---

## 🔄 PRIMARY RESUME COMMANDS

### `/resume_progress`
**Purpose**: Complete context restoration and work resumption  
**Usage**: Start of every new session  
**Scope**: Full project context

**Expected AI Response Pattern**:
```
⚡️ RESUMING CLAUDECODE PROGRESS

📊 PROJECT STATUS:
- Phase: [CURRENT_PHASE] 
- Task: [ACTIVE_TASK_ID] - [TASK_NAME]
- Progress: [PERCENTAGE]% complete
- Status: [STATUS_INDICATOR]

🎯 CURRENT CONTEXT:
[Brief description of what was being worked on]

📁 FILES IN SCOPE:
- Modified: [list of files changed]
- Pending: [list of files to create/modify]

🚦 NEXT ACTIONS:
1. [Specific immediate action]
2. [Follow-up action]
3. [Validation step]

⏱️ ESTIMATED TIME: [time estimate]

🚨 BLOCKERS: [any blocking issues or none]

Ready to proceed with [TASK_ID]? Please confirm understanding.
```

### `/resume_progress [TASK_ID]`
**Purpose**: Jump directly to specific task  
**Usage**: When you know exact task to continue  
**Scope**: Single task context

**Example**: `/resume_progress P1.1.2`

**Expected AI Response Pattern**:
```
⚡️ RESUMING TASK: [TASK_ID]

📋 TASK DETAILS:
- Name: [TASK_NAME]
- Status: [STATUS]
- Progress: [PERCENTAGE]%
- Dependencies: [list or "none"]

🎯 OBJECTIVE:
[Clear task objective description]

✅ ACCEPTANCE CRITERIA:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

🔧 IMPLEMENTATION NOTES:
[Any specific implementation details]

🚦 IMMEDIATE NEXT STEP:
[Specific action to take right now]

Ready to begin [SPECIFIC_ACTION]?
```

---

## 📊 STATUS AND MONITORING COMMANDS

### `/progress_status`
**Purpose**: Quick status check without full context load  
**Usage**: During active sessions for status updates  
**Scope**: High-level overview

**Expected AI Response Pattern**:
```
📊 QUICK STATUS UPDATE

Current: Phase [X] - [PHASE_NAME] ([PERCENTAGE]% complete)
Active Task: [TASK_ID] - [TASK_NAME] ([PERCENTAGE]% complete)
Session Progress: [X] hours, [Y] tasks advanced
Next: [BRIEF_NEXT_ACTION]
Blockers: [any issues or "none"]

Continue current work? Y/N
```

### `/validate_current_state`
**Purpose**: Verify progress state matches actual project files  
**Usage**: When suspicious of progress accuracy  
**Scope**: Reconciliation check

**Expected AI Response Pattern**:
```
🔍 STATE VALIDATION RESULTS

📁 FILE SYSTEM ANALYSIS:
- Expected files: [X] found, [Y] missing
- Unexpected files: [list or "none"]
- Modified since last checkpoint: [list or "none"]

📊 PROGRESS ACCURACY:
- Status alignment: [GOOD/ISSUES/CRITICAL]
- Task completion validation: [results]
- Dependency check: [results]

🚨 DISCREPANCIES:
[list of any mismatches or "none found"]

🔧 RECOMMENDATIONS:
[specific actions to resolve issues]

State is [VALID/NEEDS_RECONCILIATION/REQUIRES_REBUILD]
```

---

## 💾 CHECKPOINT AND SAVE COMMANDS

### `/checkpoint_save [DESCRIPTION]`
**Purpose**: Create manual progress checkpoint  
**Usage**: Before major changes, end of sessions, significant milestones  
**Scope**: Complete state preservation

**Example**: `/checkpoint_save "Completed template engine framework"`

**Expected AI Response Pattern**:
```
💾 CHECKPOINT CREATED

Checkpoint ID: CP[XXX]
Timestamp: [ISO_TIMESTAMP]
Description: [USER_DESCRIPTION]

📊 STATE CAPTURED:
- Phase: [CURRENT_PHASE]
- Task: [ACTIVE_TASK] ([PERCENTAGE]% complete)
- Files: [X] modified, [Y] created
- Context: [brief context summary]

✅ CHECKPOINT SUCCESSFUL
Recovery command: /recover_from_checkpoint CP[XXX]

Continue current work? Y/N
```

### `/auto_checkpoint_toggle`
**Purpose**: Enable/disable automatic checkpointing  
**Usage**: Configure automatic progress saving  
**Scope**: System configuration

### `/checkpoint_list`
**Purpose**: Show available checkpoints  
**Usage**: When planning recovery or reviewing history  
**Scope**: Historical data

**Expected AI Response Pattern**:
```
📋 AVAILABLE CHECKPOINTS

CP001 | 2024-12-17 10:30 | Initial progress state creation
CP002 | 2024-12-17 11:15 | Template engine framework complete  
CP003 | 2024-12-17 12:45 | Workflow orchestration implemented
[...]

Most Recent: CP[XXX] - [DESCRIPTION]
Recommended Recovery Point: CP[XXX]

Use: /recover_from_checkpoint CP[XXX] to restore
```

---

## 🚨 EMERGENCY AND RECOVERY COMMANDS

### `/recover_from_checkpoint [CHECKPOINT_ID]`
**Purpose**: Restore from specific checkpoint  
**Usage**: When normal resume fails or major issues occur  
**Scope**: Full state restoration

**Example**: `/recover_from_checkpoint CP003`

**Expected AI Response Pattern**:
```
🚨 CHECKPOINT RECOVERY INITIATED

Restoring from: CP[XXX] - [DESCRIPTION]
Timestamp: [ISO_TIMESTAMP]
Warning: Current progress since checkpoint will be lost

📊 RECOVERY STATE:
- Phase: [PHASE_FROM_CHECKPOINT]
- Task: [TASK_FROM_CHECKPOINT]
- Progress: [PERCENTAGE_FROM_CHECKPOINT]%
- Files: [files that will be restored/modified]

⚠️ IMPACT ANALYSIS:
- Work lost: [time estimate]
- Files affected: [list]
- Actions to repeat: [list]

Proceed with recovery? Y/N
If yes, type: CONFIRM_RECOVERY_CP[XXX]
```

### `/emergency_handoff`
**Purpose**: Immediate state save when context window approaching limit  
**Usage**: When hitting token limits mid-task  
**Scope**: Emergency preservation

**Expected AI Response Pattern**:
```
🚨 EMERGENCY HANDOFF INITIATED

💾 SAVING CURRENT STATE...
Checkpoint: CP[XXX] created successfully

📋 HANDOFF PACKAGE:
Current Task: [TASK_ID] - [TASK_NAME]
Progress: [PERCENTAGE]% complete
Immediate Next Action: [SPECIFIC_ACTION]
Context: [critical context summary]
Files in Progress: [list]

🔄 TO RESUME IN NEW SESSION:
1. Start new conversation
2. Run: /resume_progress
3. Confirm task: [TASK_ID]
4. Continue with: [NEXT_ACTION]

Emergency handoff complete. Start new session now.
```

### `/analyze_blocker [DESCRIPTION]`
**Purpose**: Get help when stuck on current task  
**Usage**: When progress is halted and next steps unclear  
**Scope**: Problem-solving assistance

**Example**: `/analyze_blocker "Template engine not loading configuration correctly"`

**Expected AI Response Pattern**:
```
🔍 BLOCKER ANALYSIS

Problem: [USER_DESCRIPTION]

🧠 ANALYSIS:
- Root Cause Assessment: [analysis]
- Related Systems: [affected components]
- Risk Level: [LOW/MEDIUM/HIGH/CRITICAL]

💡 POTENTIAL SOLUTIONS:
1. [Solution 1 with steps]
2. [Solution 2 with steps]  
3. [Solution 3 with steps]

🎯 RECOMMENDED APPROACH:
[Specific recommendation with reasoning]

📋 ACTION PLAN:
1. [Step 1]
2. [Step 2]  
3. [Step 3]

Would you like to proceed with recommended approach?
```

### `/rebuild_progress_from_files`
**Purpose**: Reconstruct progress state from actual project files  
**Usage**: When progress files are lost or corrupted  
**Scope**: Complete state reconstruction

**Expected AI Response Pattern**:
```
🔄 REBUILDING PROGRESS STATE

📁 SCANNING PROJECT FILES...
- Configuration files: [found/analyzed]
- Implementation files: [found/analyzed] 
- Documentation files: [found/analyzed]
- Test files: [found/analyzed]

📊 PROGRESS RECONSTRUCTION:
- Estimated Phase: [PHASE]
- Probable Current Task: [TASK_ID]
- Completion Level: [PERCENTAGE]%
- Last Activity: [estimated date/time]

⚠️ CONFIDENCE LEVEL: [LOW/MEDIUM/HIGH]
Recommendations:
- [actions to improve accuracy]
- [validation steps needed]

Proceed with reconstructed state? Y/N
```

---

## 🔄 SESSION MANAGEMENT COMMANDS

### `/session_handoff`
**Purpose**: Structured transition between sessions  
**Usage**: When planning to end current session  
**Scope**: Clean session termination

**Expected AI Response Pattern**:
```
🔄 SESSION HANDOFF PREPARATION

📊 CURRENT SESSION STATUS:
- Duration: [X] hours
- Tasks Advanced: [list]
- Progress Made: [summary]
- Files Modified: [list]

💾 CREATING HANDOFF PACKAGE...
- Checkpoint: CP[XXX] saved
- Context Summary: [brief summary]
- Next Actions: [specific steps]
- Estimated Time: [for next actions]

📋 FOR NEXT SESSION:
1. Run: /resume_progress
2. Validate: [specific validations]
3. Continue: [specific continuation point]

🎯 SESSION GOALS MET: [percentage]%
Ready for handoff? Type CONFIRM_HANDOFF to complete.
```

### `/session_summary`
**Purpose**: Generate summary of current session's work  
**Usage**: End of productive sessions, for documentation  
**Scope**: Session documentation

---

## 🔍 ANALYSIS AND PLANNING COMMANDS

### `/analyze_dependencies [TASK_ID]`
**Purpose**: Check if task dependencies are met  
**Usage**: Before starting new tasks  
**Scope**: Dependency validation

### `/estimate_effort [TASK_ID]`
**Purpose**: Get time estimates for specific tasks  
**Usage**: Planning and scheduling  
**Scope**: Single task analysis

### `/plan_next_session`
**Purpose**: Create plan for upcoming work session  
**Usage**: End of current session, planning ahead  
**Scope**: Next session preparation

---

## 🛠️ SYSTEM MAINTENANCE COMMANDS

### `/reconcile_progress_state`
**Purpose**: Sync progress files with actual project state  
**Usage**: When discrepancies are detected  
**Scope**: State synchronization

### `/cleanup_checkpoints`
**Purpose**: Remove old or unnecessary checkpoints  
**Usage**: Maintenance and storage management  
**Scope**: Checkpoint management

### `/export_progress_report`
**Purpose**: Generate comprehensive progress report  
**Usage**: Status reporting, external documentation  
**Scope**: Complete project analysis

---

## ⚠️ COMMAND USAGE GUIDELINES

### **Always Start Sessions With**
```bash
/resume_progress
```

### **Before Major Changes**
```bash
/checkpoint_save "Description of current state"
```

### **When Stuck**
```bash
/analyze_blocker "Description of issue"
```

### **Before Ending Sessions**
```bash
/session_handoff
```

### **In Emergency Situations**
```bash
/emergency_handoff
```

---

## 🔧 COMMAND SYNTAX RULES

### **Required Parameters**
- Use square brackets: `[REQUIRED_PARAM]`
- Must be provided for command to execute

### **Optional Parameters**  
- Use parentheses: `(optional_param)`
- Can be omitted, defaults will be used

### **Command Prefixes**
- All commands start with forward slash: `/`
- Case insensitive: `/resume_progress` = `/RESUME_PROGRESS`

### **Parameter Quoting**
- Use quotes for multi-word parameters: `"multiple word description"`
- Single words don't need quotes: `P1.1.2`

---

## 🎯 SUCCESS PATTERNS

### **Effective Resume Pattern**
1. `/resume_progress` - Get full context
2. Validate understanding - Confirm next steps
3. `/checkpoint_save` - Save before starting
4. Execute work - Make progress on task
5. `/checkpoint_save` - Save after progress
6. `/session_handoff` - Clean termination

### **Problem-Solving Pattern**
1. `/analyze_blocker` - Understand the issue
2. `/validate_current_state` - Check assumptions
3. Apply recommended solution
4. `/checkpoint_save` - Save after resolution
5. Continue normal workflow

### **Recovery Pattern**
1. `/checkpoint_list` - See available recoveries
2. `/recover_from_checkpoint` - Restore known good state
3. `/validate_current_state` - Confirm recovery
4. `/resume_progress` - Continue from restored point

---

**🎯 Remember**: These commands are designed to make ClaudeCode development seamless across any interruption. When in doubt, start with `/resume_progress` and follow the guidance provided.

---

*Generated by ClaudeCode Progress Continuity System v1.0*