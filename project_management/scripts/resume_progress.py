#!/usr/bin/env python3
"""
ClaudeCode Progress Resume Implementation
Implements the /resume_progress command and related progress continuity functionality.

ABOUTME: This script provides the executable implementation of the progress
continuity system, enabling seamless session resumption across context boundaries.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List
import hashlib


class ProgressManager:
    """Manages progress state, checkpoints, and session continuity."""

    def __init__(self, project_root: str = None):
        """Initialize the progress manager with project root path."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.progress_dir = self.project_root / "progress-state"
        self.state_file = self.progress_dir / "PROGRESS_STATE.json"
        self.checkpoints_dir = self.progress_dir / "checkpoints"
        self.snapshots_dir = self.progress_dir / "snapshots"

        # Ensure directories exist
        self.progress_dir.mkdir(exist_ok=True)
        self.checkpoints_dir.mkdir(exist_ok=True)
        self.snapshots_dir.mkdir(exist_ok=True)

    def load_progress_state(self) -> Dict[str, Any]:
        """Load current progress state from JSON file."""
        try:
            if not self.state_file.exists():
                return self._create_default_state()

            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️ Error loading progress state: {e}")
            return self._create_default_state()

    def save_progress_state(self, state: Dict[str, Any]) -> bool:
        """Save progress state to JSON file."""
        try:
            # Update metadata
            state["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()

            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving progress state: {e}")
            return False

    def resume_progress(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Implement /resume_progress command."""
        state = self.load_progress_state()

        if task_id:
            return self._resume_specific_task(state, task_id)
        else:
            return self._resume_current_progress(state)

    def _resume_current_progress(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Resume from current active task."""
        current_session = state.get("current_session", {})
        active_task = current_session.get("active_task", "UNKNOWN")

        # Find active task details
        task_details = self._find_task_details(state, active_task)

        # Build resume context
        resume_context = {
            "command": "/resume_progress",
            "status": "SUCCESS",
            "project_status": {
                "phase": state["metadata"].get("current_phase", 1),
                "phase_name": self._get_phase_name(state, state["metadata"].get("current_phase", 1)),
                "task": active_task,
                "task_name": task_details.get("name", "Unknown Task"),
                "progress": task_details.get("progress_percentage", 0),
                "status_indicator": task_details.get("status", "UNKNOWN")
            },
            "current_context": current_session.get("context_summary", "No context available"),
            "files_in_scope": {
                "modified": self._get_recently_modified_files(),
                "pending": task_details.get("files_pending", [])
            },
            "next_actions": self._generate_next_actions(state, task_details),
            "estimated_time": current_session.get("estimated_time_remaining", "Unknown"),
            "blockers": self._get_active_blockers(state),
            "ready_message": f"Ready to proceed with {active_task}? Please confirm understanding."
        }

        return resume_context

    def _resume_specific_task(self, state: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Resume from specific task ID."""
        task_details = self._find_task_details(state, task_id)

        if not task_details:
            return {
                "command": f"/resume_progress {task_id}",
                "status": "ERROR",
                "message": f"Task {task_id} not found in progress state",
                "suggestion": "Run /progress_status to see available tasks"
            }

        resume_context = {
            "command": f"/resume_progress {task_id}",
            "status": "SUCCESS",
            "task_details": {
                "id": task_id,
                "name": task_details.get("name", "Unknown"),
                "status": task_details.get("status", "UNKNOWN"),
                "progress": task_details.get("progress_percentage", 0),
                "dependencies": task_details.get("dependencies", [])
            },
            "objective": task_details.get("description", "No description available"),
            "acceptance_criteria": self._extract_acceptance_criteria(task_details),
            "implementation_notes": task_details.get("notes", "No implementation notes"),
            "immediate_next_step": self._get_immediate_next_step(task_details),
            "ready_message": f"Ready to begin {self._get_immediate_next_step(task_details)}?"
        }

        return resume_context

    def progress_status(self) -> Dict[str, Any]:
        """Implement /progress_status command."""
        state = self.load_progress_state()
        current_session = state.get("current_session", {})

        return {
            "command": "/progress_status",
            "status": "SUCCESS",
            "current_phase": f"Phase {state['metadata'].get('current_phase', 1)} - {self._get_phase_name(state, state['metadata'].get('current_phase', 1))}",
            "phase_progress": f"{state['metadata'].get('overall_progress', 0)}% complete",
            "active_task": f"{current_session.get('active_task', 'UNKNOWN')} - {self._get_task_name(state, current_session.get('active_task', ''))}",
            "task_progress": f"{self._get_task_progress(state, current_session.get('active_task', ''))}% complete",
            "session_progress": f"{self._calculate_session_hours(current_session)} hours, {self._count_session_tasks(state)} tasks advanced",
            "next": current_session.get("next_planned_action", "No next action defined"),
            "blockers": "none" if not self._get_active_blockers(state) else str(len(self._get_active_blockers(state))) + " active",
            "continue_prompt": "Continue current work? Y/N"
        }

    def checkpoint_save(self, description: str) -> Dict[str, Any]:
        """Implement /checkpoint_save command."""
        state = self.load_progress_state()

        # Generate checkpoint ID
        checkpoint_count = len(state.get("checkpoints", [])) + 1
        checkpoint_id = f"CP{checkpoint_count:03d}"

        # Create checkpoint data
        checkpoint = {
            "checkpoint_id": checkpoint_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "description": description,
            "phase": state["metadata"].get("current_phase", 1),
            "task": state["current_session"].get("active_task", "UNKNOWN"),
            "completion_percentage": state["metadata"].get("overall_progress", 0),
            "files_modified": state["current_session"].get("files_modified", []),
            "context_snapshot": state["current_session"].get("context_summary", ""),
            "next_actions": self._generate_next_actions(state, self._find_task_details(state, state["current_session"].get("active_task", "")))
        }

        # Save checkpoint to file
        checkpoint_file = self.checkpoints_dir / f"{checkpoint_id}_{datetime.now().strftime('%Y%m%d_%H%M')}_{self._slugify(description)}.json"

        try:
            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "checkpoint": checkpoint,
                    "full_state": state
                }, f, indent=2, ensure_ascii=False)

            # Add to checkpoints list in state
            if "checkpoints" not in state:
                state["checkpoints"] = []
            state["checkpoints"].append(checkpoint)

            # Update recovery info
            state["recovery"]["last_known_good_state"] = checkpoint_id
            state["recovery"]["recovery_instructions"] = f"Load checkpoint {checkpoint_id} and resume from {checkpoint['task']}"

            # Save updated state
            self.save_progress_state(state)

            return {
                "command": f"/checkpoint_save \"{description}\"",
                "status": "SUCCESS",
                "checkpoint_id": checkpoint_id,
                "timestamp": checkpoint["timestamp"],
                "description": description,
                "state_captured": {
                    "phase": checkpoint["phase"],
                    "task": f"{checkpoint['task']} ({checkpoint['completion_percentage']}% complete)",
                    "files": f"{len(checkpoint['files_modified'])} modified",
                    "context": checkpoint["context_snapshot"][:100] + "..." if len(checkpoint["context_snapshot"]) > 100 else checkpoint["context_snapshot"]
                },
                "checkpoint_successful": True,
                "recovery_command": f"/recover_from_checkpoint {checkpoint_id}",
                "continue_prompt": "Continue current work? Y/N"
            }

        except Exception as e:
            return {
                "command": f"/checkpoint_save \"{description}\"",
                "status": "ERROR",
                "message": f"Failed to create checkpoint: {e}",
                "suggestion": "Check file permissions and disk space"
            }

    def analyze_blocker(self, description: str) -> Dict[str, Any]:
        """Implement /analyze_blocker command."""
        state = self.load_progress_state()
        current_task = state["current_session"].get("active_task", "")
        task_details = self._find_task_details(state, current_task)

        # Basic blocker analysis (can be enhanced with AI integration)
        analysis = {
            "command": f"/analyze_blocker \"{description}\"",
            "status": "SUCCESS",
            "problem": description,
            "analysis": {
                "root_cause_assessment": self._analyze_root_cause(description, task_details),
                "related_systems": self._identify_related_systems(description, state),
                "risk_level": self._assess_risk_level(description)
            },
            "potential_solutions": self._generate_solutions(description, task_details),
            "recommended_approach": self._recommend_approach(description, task_details),
            "action_plan": self._create_action_plan(description, task_details),
            "continue_prompt": "Would you like to proceed with recommended approach?"
        }

        return analysis

    def _create_default_state(self) -> Dict[str, Any]:
        """Create default progress state structure."""
        return {
            "metadata": {
                "version": "1.0",
                "created": datetime.now(timezone.utc).isoformat(),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "updated_by": "ProgressManager",
                "project_name": "ClaudeCode Enhancement",
                "total_phases": 5,
                "current_phase": 1,
                "overall_progress": 0.0
            },
            "current_session": {
                "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M')}",
                "started": datetime.now(timezone.utc).isoformat(),
                "last_activity": datetime.now(timezone.utc).isoformat(),
                "active_task": "P1.1.1",
                "context_summary": "Project initialization",
                "next_planned_action": "Begin project setup",
                "estimated_time_remaining": "Unknown",
                "checkpoint_frequency": 30
            },
            "phases": {},
            "blockers": {"active": [], "resolved": []},
            "decisions": {"pending": [], "made": []},
            "metrics": {
                "total_tasks": 0,
                "completed_tasks": 0,
                "in_progress_tasks": 0,
                "blocked_tasks": 0,
                "total_estimated_hours": 0,
                "hours_completed": 0,
                "current_velocity": 0.0,
                "projected_completion": "TBD"
            },
            "checkpoints": [],
            "recovery": {
                "last_known_good_state": None,
                "rollback_available": False,
                "recovery_instructions": "No recovery points available",
                "emergency_contacts": [],
                "backup_locations": ["ClaudeCode/progress-state/backups/"]
            }
        }

    def _find_task_details(self, state: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Find task details by ID in the state structure."""
        phases = state.get("phases", {})

        for phase_id, phase_data in phases.items():
            tasks = phase_data.get("tasks", {})
            for task_key, task_data in tasks.items():
                if task_key == task_id:
                    return task_data

                # Check subtasks
                subtasks = task_data.get("subtasks", {})
                for subtask_key, subtask_data in subtasks.items():
                    if subtask_key == task_id:
                        return subtask_data

        return {}

    def _get_phase_name(self, state: Dict[str, Any], phase_num: int) -> str:
        """Get phase name by number."""
        phase_names = {
            1: "Foundation & Continuity",
            2: "Core Feature Implementation",
            3: "Boundary Definition & Guardrails",
            4: "Language Agnostic Expansion",
            5: "Advanced Features & Optimization"
        }
        return phase_names.get(phase_num, f"Phase {phase_num}")

    def _get_recently_modified_files(self) -> List[str]:
        """Get list of recently modified files."""
        # This would scan the project directory for recent changes
        # For now, return empty list - can be enhanced
        return []

    def _generate_next_actions(self, state: Dict[str, Any], task_details: Dict[str, Any]) -> List[str]:
        """Generate next actions based on current state."""
        if not task_details:
            return ["Review current task status", "Update progress state", "Continue with planned work"]

        status = task_details.get("status", "UNKNOWN")
        if status == "IN_PROGRESS":
            return [
                f"Continue working on {task_details.get('name', 'current task')}",
                "Update progress as work proceeds",
                "Create checkpoint after significant progress"
            ]
        elif status == "PENDING":
            return [
                f"Begin work on {task_details.get('name', 'planned task')}",
                "Review acceptance criteria",
                "Create initial checkpoint"
            ]
        else:
            return ["Review task status", "Determine next steps", "Update progress state"]

    def _get_active_blockers(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get list of active blockers."""
        return state.get("blockers", {}).get("active", [])

    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        import re
        text = re.sub(r'[^\w\s-]', '', text).strip().lower()
        return re.sub(r'[\s_-]+', '-', text)[:50]

    # Additional helper methods for blocker analysis
    def _analyze_root_cause(self, description: str, task_details: Dict[str, Any]) -> str:
        """Analyze potential root cause of blocker."""
        if "file" in description.lower() or "import" in description.lower():
            return "Likely file system or dependency issue"
        elif "config" in description.lower():
            return "Configuration or setup problem"
        elif "test" in description.lower():
            return "Testing or validation issue"
        else:
            return "Requires detailed analysis of the specific problem"

    def _identify_related_systems(self, description: str, state: Dict[str, Any]) -> List[str]:
        """Identify systems related to the blocker."""
        systems = []
        if "template" in description.lower():
            systems.append("Template Engine")
        if "progress" in description.lower():
            systems.append("Progress Tracking")
        if "config" in description.lower():
            systems.append("Configuration System")
        return systems if systems else ["Unknown System"]

    def _assess_risk_level(self, description: str) -> str:
        """Assess risk level of the blocker."""
        high_risk_keywords = ["critical", "failure", "crash", "data loss"]
        medium_risk_keywords = ["error", "broken", "not working"]

        desc_lower = description.lower()
        if any(keyword in desc_lower for keyword in high_risk_keywords):
            return "HIGH"
        elif any(keyword in desc_lower for keyword in medium_risk_keywords):
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_solutions(self, description: str, task_details: Dict[str, Any]) -> List[str]:
        """Generate potential solutions for the blocker."""
        return [
            "Review error messages and logs for specific details",
            "Check configuration files and dependencies",
            "Validate current environment and setup",
            "Consult documentation and examples",
            "Create minimal reproduction case"
        ]

    def _recommend_approach(self, description: str, task_details: Dict[str, Any]) -> str:
        """Recommend best approach for resolving blocker."""
        return "Start with detailed error analysis, then check configuration and dependencies systematically"

    def _create_action_plan(self, description: str, task_details: Dict[str, Any]) -> List[str]:
        """Create specific action plan for resolving blocker."""
        return [
            "Document exact error messages and symptoms",
            "Check related configuration files",
            "Verify dependencies and imports",
            "Test with minimal example",
            "Apply fix and validate resolution"
        ]

    # Additional helper methods
    def _extract_acceptance_criteria(self, task_details: Dict[str, Any]) -> List[str]:
        """Extract acceptance criteria from task details."""
        # This would parse acceptance criteria from task details
        return ["Acceptance criteria not defined"]

    def _get_immediate_next_step(self, task_details: Dict[str, Any]) -> str:
        """Get immediate next step for task."""
        return task_details.get("next_step", "Continue with task implementation")

    def _get_task_name(self, state: Dict[str, Any], task_id: str) -> str:
        """Get task name by ID."""
        task_details = self._find_task_details(state, task_id)
        return task_details.get("name", "Unknown Task")

    def _get_task_progress(self, state: Dict[str, Any], task_id: str) -> int:
        """Get task progress percentage by ID."""
        task_details = self._find_task_details(state, task_id)
        return task_details.get("progress_percentage", 0)

    def _calculate_session_hours(self, session: Dict[str, Any]) -> float:
        """Calculate hours spent in current session."""
        # This would calculate actual time - for now return placeholder
        return 2.5

    def _count_session_tasks(self, state: Dict[str, Any]) -> int:
        """Count tasks advanced in current session."""
        # This would count actual tasks - for now return placeholder
        return 1


def main():
    """Main entry point for the progress resume script."""
    if len(sys.argv) < 2:
        print("Usage: python resume_progress.py <command> [args...]")
        print("Commands: resume_progress, progress_status, checkpoint_save, analyze_blocker")
        sys.exit(1)

    command = sys.argv[1]
    manager = ProgressManager()

    try:
        if command == "resume_progress":
            task_id = sys.argv[2] if len(sys.argv) > 2 else None
            result = manager.resume_progress(task_id)
        elif command == "progress_status":
            result = manager.progress_status()
        elif command == "checkpoint_save":
            description = sys.argv[2] if len(sys.argv) > 2 else "Manual checkpoint"
            result = manager.checkpoint_save(description)
        elif command == "analyze_blocker":
            description = sys.argv[2] if len(sys.argv) > 2 else "Unspecified blocker"
            result = manager.analyze_blocker(description)
        else:
            result = {"status": "ERROR", "message": f"Unknown command: {command}"}

        # Pretty print the result
        print("⚡️ CLAUDECODE PROGRESS SYSTEM")
        print("=" * 50)

        if result.get("status") == "SUCCESS":
            if command == "resume_progress":
                if "project_status" in result:
                    print(f"\n📊 PROJECT STATUS:")
                    ps = result["project_status"]
                    print(f"- Phase: {ps['phase']} - {ps['phase_name']}")
                    print(f"- Task: {ps['task']} - {ps['task_name']}")
                    print(f"- Progress: {ps['progress']}% complete")
                    print(f"- Status: {ps['status_indicator']}")

                    print(f"\n🎯 CURRENT CONTEXT:")
                    print(f"{result['current_context']}")

                    print(f"\n📁 FILES IN SCOPE:")
                    files = result["files_in_scope"]
                    if files["modified"]:
                        print(f"- Modified: {', '.join(files['modified'])}")
                    if files["pending"]:
                        print(f"- Pending: {', '.join(files['pending'])}")

                    print(f"\n🚦 NEXT ACTIONS:")
                    for i, action in enumerate(result["next_actions"], 1):
                        print(f"{i}. {action}")

                    print(f"\n⏱️ ESTIMATED TIME: {result['estimated_time']}")
                    print(f"🚨 BLOCKERS: {result['blockers'] if result['blockers'] else 'None'}")
                    print(f"\n{result['ready_message']}")

                elif "task_details" in result:
                    print(f"\n📋 TASK DETAILS:")
                    td = result["task_details"]
                    print(f"- Name: {td['name']}")
                    print(f"- Status: {td['status']}")
                    print(f"- Progress: {td['progress']}%")
                    print(f"- Dependencies: {', '.join(td['dependencies']) if td['dependencies'] else 'None'}")

                    print(f"\n🎯 OBJECTIVE:")
                    print(f"{result['objective']}")

                    print(f"\n🚦 IMMEDIATE NEXT STEP:")
                    print(f"{result['immediate_next_step']}")

                    print(f"\n{result['ready_message']}")

            elif command == "progress_status":
                print(f"\n📊 QUICK STATUS UPDATE")
                print(f"Current: {result['current_phase']} ({result['phase_progress']})")
                print(f"Active Task: {result['active_task']} ({result['task_progress']})")
                print(f"Session Progress: {result['session_progress']}")
                print(f"Next: {result['next']}")
                print(f"Blockers: {result['blockers']}")
                print(f"\n{result['continue_prompt']}")

            elif command == "checkpoint_save":
                print(f"\n💾 CHECKPOINT CREATED")
                print(f"Checkpoint ID: {result['checkpoint_id']}")
                print(f"Timestamp: {result['timestamp']}")
                print(f"Description: {result['description']}")

                print(f"\n📊 STATE CAPTURED:")
                sc = result["state_captured"]
                print(f"- Phase: {sc['phase']}")
                print(f"- Task: {sc['task']}")
                print(f"- Files: {sc['files']}")
                print(f"- Context: {sc['context']}")

                print(f"\n✅ CHECKPOINT SUCCESSFUL")
                print(f"Recovery command: {result['recovery_command']}")
                print(f"\n{result['continue_prompt']}")

            elif command == "analyze_blocker":
                print(f"\n🔍 BLOCKER ANALYSIS")
                print(f"Problem: {result['problem']}")

                print(f"\n🧠 ANALYSIS:")
                analysis = result["analysis"]
                print(f"- Root Cause Assessment: {analysis['root_cause_assessment']}")
                print(f"- Related Systems: {', '.join(analysis['related_systems'])}")
                print(f"- Risk Level: {analysis['risk_level']}")

                print(f"\n💡 POTENTIAL SOLUTIONS:")
                for i, solution in enumerate(result["potential_solutions"], 1):
                    print(f"{i}. {solution}")

                print(f"\n🎯 RECOMMENDED APPROACH:")
                print(f"{result['recommended_approach']}")

                print(f"\n📋 ACTION PLAN:")
                for i, step in enumerate(result["action_plan"], 1):
                    print(f"{i}. {step}")

                print(f"\n{result['continue_prompt']}")

        else:
            print(f"❌ ERROR: {result.get('message', 'Unknown error')}")
            if "suggestion" in result:
                print(f"💡 Suggestion: {result['suggestion']}")

    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
