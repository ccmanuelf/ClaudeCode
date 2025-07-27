#!/usr/bin/env python3
"""
ClaudeCode Command Wrapper
Provides easy-to-use commands for ClaudeCode progress continuity system.

ABOUTME: This wrapper script enables the /resume_progress and related commands
to function as simple command-line tools integrated with ClaudeCode.
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from resume_progress import ProgressManager
except ImportError:
    print("❌ Error: Could not import ProgressManager")
    print("Make sure resume_progress.py is in the same directory")
    sys.exit(1)


def print_header(title: str):
    """Print formatted header for command output."""
    print("⚡️ CLAUDECODE PROGRESS SYSTEM")
    print("=" * 50)
    print(f"{title}")
    print("-" * 50)


def handle_resume_progress(args):
    """Handle /resume_progress command."""
    manager = ProgressManager()

    if len(args) > 1:
        # Specific task resume
        task_id = args[1]
        result = manager.resume_progress(task_id)

        print_header(f"RESUMING TASK: {task_id}")

        if result.get("status") == "SUCCESS":
            td = result["task_details"]
            print(f"\n📋 TASK DETAILS:")
            print(f"- Name: {td['name']}")
            print(f"- Status: {td['status']}")
            print(f"- Progress: {td['progress']}%")
            print(f"- Dependencies: {', '.join(td['dependencies']) if td['dependencies'] else 'None'}")

            print(f"\n🎯 OBJECTIVE:")
            print(f"{result['objective']}")

            print(f"\n🚦 IMMEDIATE NEXT STEP:")
            print(f"{result['immediate_next_step']}")

            print(f"\n{result['ready_message']}")
        else:
            print(f"❌ ERROR: {result.get('message', 'Unknown error')}")
            if "suggestion" in result:
                print(f"💡 {result['suggestion']}")
    else:
        # General resume
        result = manager.resume_progress()

        print_header("RESUMING CLAUDECODE PROGRESS")

        if result.get("status") == "SUCCESS":
            ps = result["project_status"]
            print(f"\n📊 PROJECT STATUS:")
            print(f"- Phase: {ps['phase']} - {ps['phase_name']}")
            print(f"- Task: {ps['task']} - {ps['task_name']}")
            print(f"- Progress: {ps['progress']}% complete")
            print(f"- Status: {ps['status_indicator']}")

            print(f"\n🎯 CURRENT CONTEXT:")
            print(f"{result['current_context']}")

            files = result["files_in_scope"]
            print(f"\n📁 FILES IN SCOPE:")
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


def handle_progress_status(args):
    """Handle /progress_status command."""
    manager = ProgressManager()
    result = manager.progress_status()

    print_header("QUICK STATUS UPDATE")

    if result.get("status") == "SUCCESS":
        print(f"\nCurrent: {result['current_phase']} ({result['phase_progress']})")
        print(f"Active Task: {result['active_task']} ({result['task_progress']})")
        print(f"Session Progress: {result['session_progress']}")
        print(f"Next: {result['next']}")
        print(f"Blockers: {result['blockers']}")
        print(f"\n{result['continue_prompt']}")


def handle_checkpoint_save(args):
    """Handle /checkpoint_save command."""
    if len(args) < 2:
        print("Usage: /checkpoint_save \"Description of current state\"")
        return

    description = " ".join(args[1:]).strip('"\'')
    manager = ProgressManager()
    result = manager.checkpoint_save(description)

    print_header("CHECKPOINT CREATION")

    if result.get("status") == "SUCCESS":
        print(f"\n💾 CHECKPOINT CREATED")
        print(f"Checkpoint ID: {result['checkpoint_id']}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Description: {result['description']}")

        sc = result["state_captured"]
        print(f"\n📊 STATE CAPTURED:")
        print(f"- Phase: {sc['phase']}")
        print(f"- Task: {sc['task']}")
        print(f"- Files: {sc['files']}")
        print(f"- Context: {sc['context']}")

        print(f"\n✅ CHECKPOINT SUCCESSFUL")
        print(f"Recovery command: {result['recovery_command']}")
        print(f"\n{result['continue_prompt']}")
    else:
        print(f"❌ ERROR: {result.get('message', 'Unknown error')}")


def handle_analyze_blocker(args):
    """Handle /analyze_blocker command."""
    if len(args) < 2:
        print("Usage: /analyze_blocker \"Description of what you're stuck on\"")
        return

    description = " ".join(args[1:]).strip('"\'')
    manager = ProgressManager()
    result = manager.analyze_blocker(description)

    print_header("BLOCKER ANALYSIS")

    if result.get("status") == "SUCCESS":
        print(f"\nProblem: {result['problem']}")

        analysis = result["analysis"]
        print(f"\n🧠 ANALYSIS:")
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


def show_help():
    """Show available commands and usage."""
    print_header("CLAUDECODE COMMANDS HELP")

    print(f"\n📋 AVAILABLE COMMANDS:")
    print(f"  /resume_progress [task_id]  - Resume work from current or specific task")
    print(f"  /progress_status            - Quick status check")
    print(f"  /checkpoint_save \"desc\"     - Create manual checkpoint")
    print(f"  /analyze_blocker \"issue\"    - Get help when stuck")
    print(f"  /help                       - Show this help message")

    print(f"\n💡 EXAMPLES:")
    print(f"  python claudecode_commands.py /resume_progress")
    print(f"  python claudecode_commands.py /resume_progress P1.1.2")
    print(f"  python claudecode_commands.py /checkpoint_save \"Template engine complete\"")
    print(f"  python claudecode_commands.py /analyze_blocker \"Config file not loading\"")

    print(f"\n🎯 QUICK START:")
    print(f"  1. Run '/resume_progress' to get current status")
    print(f"  2. Follow the generated action plan")
    print(f"  3. Save checkpoints with '/checkpoint_save' regularly")
    print(f"  4. Use '/analyze_blocker' when stuck")


def main():
    """Main entry point for ClaudeCode commands."""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    command = sys.argv[1].lower()
    args = sys.argv[1:]  # Include command in args for consistency

    try:
        if command in ['/resume_progress', 'resume_progress']:
            handle_resume_progress(args)
        elif command in ['/progress_status', 'progress_status']:
            handle_progress_status(args)
        elif command in ['/checkpoint_save', 'checkpoint_save']:
            handle_checkpoint_save(args)
        elif command in ['/analyze_blocker', 'analyze_blocker']:
            handle_analyze_blocker(args)
        elif command in ['/help', 'help', '-h', '--help']:
            show_help()
        else:
            print(f"❌ Unknown command: {command}")
            print(f"Run 'python claudecode_commands.py /help' for available commands")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n\n👋 ClaudeCode session interrupted. Progress has been saved.")
        print(f"Run '/resume_progress' to continue where you left off.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")
        print(f"💡 Try running '/help' for usage information")
        sys.exit(1)


if __name__ == "__main__":
    main()
