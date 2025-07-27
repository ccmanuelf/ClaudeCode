#!/usr/bin/env python3
"""
ClaudeCode Checkpoint Recovery System
Provides comprehensive checkpoint recovery and state restoration functionality.

ABOUTME: This script handles all aspects of checkpoint recovery, including
state validation, file restoration, and recovery from various failure scenarios.
"""

import json
import os
import sys
import shutil
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CheckpointRecovery')


class CheckpointRecoveryManager:
    """Manages checkpoint recovery and state restoration operations."""

    def __init__(self, project_root: str = None):
        """Initialize the recovery manager."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.progress_dir = self.project_root / "progress-state"
        self.state_file = self.progress_dir / "PROGRESS_STATE.json"
        self.checkpoints_dir = self.progress_dir / "checkpoints"
        self.snapshots_dir = self.progress_dir / "snapshots"
        self.backup_dir = self.progress_dir / "backups"
        self.recovery_log = self.progress_dir / "recovery.log"

        # Ensure directories exist
        self.progress_dir.mkdir(exist_ok=True)
        self.checkpoints_dir.mkdir(exist_ok=True)
        self.snapshots_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)

    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """List all available checkpoints with metadata."""
        checkpoints = []

        try:
            for checkpoint_file in self.checkpoints_dir.glob('*.json'):
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    checkpoint_info = data.get('checkpoint', {})

                    checkpoints.append({
                        'id': checkpoint_info.get('checkpoint_id', 'UNKNOWN'),
                        'timestamp': checkpoint_info.get('timestamp', ''),
                        'description': checkpoint_info.get('description', ''),
                        'type': checkpoint_info.get('type', 'MANUAL'),
                        'phase': checkpoint_info.get('phase', 0),
                        'task': checkpoint_info.get('task', ''),
                        'progress': checkpoint_info.get('completion_percentage', 0),
                        'file': str(checkpoint_file),
                        'file_size': checkpoint_file.stat().st_size,
                        'validation_status': checkpoint_info.get('validation_status', 'UNKNOWN')
                    })

        except Exception as e:
            logger.error(f"Error listing checkpoints: {e}")

        # Sort by timestamp, newest first
        checkpoints.sort(key=lambda x: x['timestamp'], reverse=True)
        return checkpoints

    def validate_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        """Validate checkpoint integrity and completeness."""
        validation_result = {
            'checkpoint_id': checkpoint_id,
            'valid': False,
            'issues': [],
            'warnings': [],
            'file_checks': {},
            'data_integrity': False,
            'recovery_feasible': False
        }

        try:
            # Find checkpoint file
            checkpoint_file = self._find_checkpoint_file(checkpoint_id)
            if not checkpoint_file:
                validation_result['issues'].append(f"Checkpoint file not found for {checkpoint_id}")
                return validation_result

            # Load checkpoint data
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint_data = json.load(f)

            checkpoint_info = checkpoint_data.get('checkpoint', {})
            full_state = checkpoint_data.get('full_state', {})

            # Validate checkpoint structure
            required_fields = ['checkpoint_id', 'timestamp', 'description', 'phase', 'task']
            missing_fields = [field for field in required_fields if field not in checkpoint_info]

            if missing_fields:
                validation_result['issues'].append(f"Missing required fields: {', '.join(missing_fields)}")
            else:
                validation_result['data_integrity'] = True

            # Validate full state structure
            required_state_sections = ['metadata', 'current_session', 'phases']
            missing_sections = [section for section in required_state_sections if section not in full_state]

            if missing_sections:
                validation_result['warnings'].append(f"Missing state sections: {', '.join(missing_sections)}")

            # Check file references
            files_modified = checkpoint_info.get('files_modified', [])
            files_created = checkpoint_info.get('files_created', [])
            all_files = files_modified + files_created

            for file_path in all_files:
                full_path = self.project_root / file_path
                validation_result['file_checks'][file_path] = {
                    'exists': full_path.exists(),
                    'readable': full_path.exists() and os.access(full_path, os.R_OK),
                    'size': full_path.stat().st_size if full_path.exists() else 0
                }

            # Calculate overall validation status
            has_critical_issues = len(validation_result['issues']) > 0
            has_file_issues = any(not check['exists'] for check in validation_result['file_checks'].values())

            validation_result['valid'] = not has_critical_issues and validation_result['data_integrity']
            validation_result['recovery_feasible'] = validation_result['valid'] and not has_file_issues

            if has_file_issues:
                validation_result['warnings'].append("Some referenced files are missing or inaccessible")

        except json.JSONDecodeError as e:
            validation_result['issues'].append(f"Checkpoint file is corrupted: {e}")
        except Exception as e:
            validation_result['issues'].append(f"Validation error: {e}")

        return validation_result

    def recover_from_checkpoint(self, checkpoint_id: str, confirm: bool = False) -> Dict[str, Any]:
        """Recover system state from specified checkpoint."""
        recovery_result = {
            'checkpoint_id': checkpoint_id,
            'success': False,
            'backup_created': False,
            'files_restored': [],
            'files_failed': [],
            'state_restored': False,
            'recovery_time': datetime.now(timezone.utc).isoformat(),
            'messages': []
        }

        try:
            # Validate checkpoint first
            validation = self.validate_checkpoint(checkpoint_id)
            if not validation['recovery_feasible']:
                recovery_result['messages'].append("Checkpoint validation failed")
                recovery_result['messages'].extend(validation['issues'])
                return recovery_result

            # Find checkpoint file
            checkpoint_file = self._find_checkpoint_file(checkpoint_id)
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint_data = json.load(f)

            checkpoint_info = checkpoint_data.get('checkpoint', {})
            full_state = checkpoint_data.get('full_state', {})

            # Create backup of current state before recovery
            backup_success = self._create_recovery_backup()
            recovery_result['backup_created'] = backup_success

            if not backup_success:
                recovery_result['messages'].append("Warning: Could not create recovery backup")

            # Restore progress state
            try:
                # Update metadata to reflect recovery
                full_state['metadata']['last_updated'] = datetime.now(timezone.utc).isoformat()
                full_state['current_session']['session_id'] = f"recovery_{datetime.now().strftime('%Y%m%d_%H%M')}"
                full_state['current_session']['last_activity'] = datetime.now(timezone.utc).isoformat()

                # Add recovery information
                if 'recovery_history' not in full_state:
                    full_state['recovery_history'] = []

                full_state['recovery_history'].append({
                    'recovered_from': checkpoint_id,
                    'recovery_time': recovery_result['recovery_time'],
                    'previous_state_backed_up': backup_success
                })

                # Save restored state
                with open(self.state_file, 'w', encoding='utf-8') as f:
                    json.dump(full_state, f, indent=2, ensure_ascii=False)

                recovery_result['state_restored'] = True
                recovery_result['messages'].append("Progress state restored successfully")

            except Exception as e:
                recovery_result['messages'].append(f"Failed to restore progress state: {e}")

            # Restore files if snapshots exist
            files_to_restore = checkpoint_info.get('files_modified', []) + checkpoint_info.get('files_created', [])

            for file_path in files_to_restore:
                try:
                    # Look for file snapshot
                    snapshot_path = self.snapshots_dir / checkpoint_id / file_path
                    if snapshot_path.exists():
                        target_path = self.project_root / file_path
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(snapshot_path, target_path)
                        recovery_result['files_restored'].append(file_path)
                    else:
                        recovery_result['messages'].append(f"No snapshot found for {file_path}")

                except Exception as e:
                    recovery_result['files_failed'].append(file_path)
                    recovery_result['messages'].append(f"Failed to restore {file_path}: {e}")

            # Log recovery operation
            self._log_recovery_operation(checkpoint_id, recovery_result)

            # Determine overall success
            recovery_result['success'] = (
                recovery_result['state_restored'] and
                len(recovery_result['files_failed']) == 0
            )

            if recovery_result['success']:
                recovery_result['messages'].append(f"Recovery from {checkpoint_id} completed successfully")
            else:
                recovery_result['messages'].append(f"Recovery from {checkpoint_id} completed with issues")

        except Exception as e:
            recovery_result['messages'].append(f"Recovery failed: {e}")
            logger.error(f"Recovery error: {e}")

        return recovery_result

    def emergency_recovery(self) -> Dict[str, Any]:
        """Perform emergency recovery from the most recent valid checkpoint."""
        checkpoints = self.list_checkpoints()

        if not checkpoints:
            return {
                'success': False,
                'message': 'No checkpoints available for emergency recovery'
            }

        # Try checkpoints in order of recency
        for checkpoint in checkpoints:
            validation = self.validate_checkpoint(checkpoint['id'])
            if validation['recovery_feasible']:
                logger.info(f"Attempting emergency recovery from {checkpoint['id']}")
                return self.recover_from_checkpoint(checkpoint['id'], confirm=True)

        return {
            'success': False,
            'message': 'No valid checkpoints found for emergency recovery'
        }

    def rebuild_from_files(self) -> Dict[str, Any]:
        """Rebuild progress state by analyzing project files."""
        rebuild_result = {
            'success': False,
            'confidence': 'LOW',
            'estimated_progress': 0,
            'detected_phase': 1,
            'probable_task': 'UNKNOWN',
            'files_analyzed': 0,
            'reconstruction_notes': []
        }

        try:
            # Analyze project structure
            config_file = self.project_root / 'config.yaml'
            if config_file.exists():
                rebuild_result['reconstruction_notes'].append("Found config.yaml - project structure intact")
                rebuild_result['confidence'] = 'MEDIUM'

            # Analyze progress-state directory
            progress_files = list(self.progress_dir.glob('*.md'))
            if progress_files:
                rebuild_result['reconstruction_notes'].append(f"Found {len(progress_files)} progress documentation files")
                rebuild_result['confidence'] = 'MEDIUM'

            # Analyze implementation files
            script_files = list((self.project_root / 'scripts').glob('*.py')) if (self.project_root / 'scripts').exists() else []
            if script_files:
                rebuild_result['reconstruction_notes'].append(f"Found {len(script_files)} implementation scripts")
                rebuild_result['files_analyzed'] = len(script_files)

                # Estimate progress based on file count and complexity
                if len(script_files) >= 3:
                    rebuild_result['estimated_progress'] = min(25, len(script_files) * 5)
                    rebuild_result['detected_phase'] = 1
                    rebuild_result['probable_task'] = 'P1.1.3'

            # Look for resume.py as indicator of progress
            resume_file = self.project_root / 'resume.py'
            if resume_file.exists():
                rebuild_result['reconstruction_notes'].append("Found resume.py - progress system partially implemented")
                rebuild_result['estimated_progress'] = max(rebuild_result['estimated_progress'], 15)
                rebuild_result['confidence'] = 'HIGH'

            # Create reconstructed state
            reconstructed_state = {
                'metadata': {
                    'version': '1.0',
                    'created': datetime.now(timezone.utc).isoformat(),
                    'last_updated': datetime.now(timezone.utc).isoformat(),
                    'updated_by': 'Recovery System',
                    'project_name': 'ClaudeCode Enhancement',
                    'total_phases': 5,
                    'current_phase': rebuild_result['detected_phase'],
                    'overall_progress': rebuild_result['estimated_progress'],
                    'reconstruction_source': 'FILE_ANALYSIS'
                },
                'current_session': {
                    'session_id': f"rebuilt_{datetime.now().strftime('%Y%m%d_%H%M')}",
                    'started': datetime.now(timezone.utc).isoformat(),
                    'last_activity': datetime.now(timezone.utc).isoformat(),
                    'active_task': rebuild_result['probable_task'],
                    'context_summary': f"State rebuilt from file analysis. Confidence: {rebuild_result['confidence']}",
                    'next_planned_action': 'Validate reconstructed state and continue development',
                    'estimated_time_remaining': 'Unknown - verify progress',
                    'checkpoint_frequency': 30
                },
                'rebuild_info': {
                    'rebuild_timestamp': datetime.now(timezone.utc).isoformat(),
                    'confidence_level': rebuild_result['confidence'],
                    'files_analyzed': rebuild_result['files_analyzed'],
                    'reconstruction_notes': rebuild_result['reconstruction_notes']
                }
            }

            # Save reconstructed state
            backup_path = self.backup_dir / f"corrupted_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            if self.state_file.exists():
                shutil.copy2(self.state_file, backup_path)

            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(reconstructed_state, f, indent=2, ensure_ascii=False)

            rebuild_result['success'] = True
            rebuild_result['reconstruction_notes'].append("Reconstructed state saved successfully")

        except Exception as e:
            rebuild_result['reconstruction_notes'].append(f"Rebuild failed: {e}")
            logger.error(f"Rebuild error: {e}")

        return rebuild_result

    def _find_checkpoint_file(self, checkpoint_id: str) -> Optional[Path]:
        """Find checkpoint file by ID."""
        for checkpoint_file in self.checkpoints_dir.glob('*.json'):
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('checkpoint', {}).get('checkpoint_id') == checkpoint_id:
                        return checkpoint_file
            except Exception:
                continue
        return None

    def _create_recovery_backup(self) -> bool:
        """Create backup of current state before recovery."""
        try:
            if not self.state_file.exists():
                return True  # Nothing to backup

            backup_filename = f"pre_recovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_path = self.backup_dir / backup_filename

            shutil.copy2(self.state_file, backup_path)
            logger.info(f"Created recovery backup: {backup_filename}")
            return True

        except Exception as e:
            logger.error(f"Failed to create recovery backup: {e}")
            return False

    def _log_recovery_operation(self, checkpoint_id: str, result: Dict[str, Any]):
        """Log recovery operation details."""
        try:
            log_entry = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'operation': 'CHECKPOINT_RECOVERY',
                'checkpoint_id': checkpoint_id,
                'success': result['success'],
                'files_restored': len(result['files_restored']),
                'files_failed': len(result['files_failed']),
                'messages': result['messages']
            }

            with open(self.recovery_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')

        except Exception as e:
            logger.error(f"Failed to log recovery operation: {e}")


def main():
    """Main entry point for checkpoint recovery operations."""
    if len(sys.argv) < 2:
        print("Usage: python checkpoint_recovery.py <command> [args...]")
        print("Commands:")
        print("  list                           # List available checkpoints")
        print("  validate <checkpoint_id>       # Validate checkpoint")
        print("  recover <checkpoint_id>        # Recover from checkpoint")
        print("  emergency                      # Emergency recovery")
        print("  rebuild                        # Rebuild from files")
        print("  help                           # Show this help")
        sys.exit(1)

    command = sys.argv[1].lower()
    recovery_manager = CheckpointRecoveryManager()

    try:
        if command == "list":
            checkpoints = recovery_manager.list_checkpoints()

            print("⚡️ AVAILABLE CHECKPOINTS")
            print("=" * 60)

            if not checkpoints:
                print("No checkpoints found.")
                return

            for cp in checkpoints:
                status_icon = "✅" if cp['validation_status'] == 'VALID' else "❓"
                type_icon = "🤖" if cp['type'] == 'AUTO' else "👤"

                print(f"{status_icon} {type_icon} {cp['id']} | {cp['timestamp'][:19]}")
                print(f"    📝 {cp['description']}")
                print(f"    📊 Phase {cp['phase']} | Task: {cp['task']} | Progress: {cp['progress']}%")
                print(f"    💾 {cp['file_size']} bytes")
                print()

        elif command == "validate":
            if len(sys.argv) < 3:
                print("Usage: python checkpoint_recovery.py validate <checkpoint_id>")
                return

            checkpoint_id = sys.argv[2]
            result = recovery_manager.validate_checkpoint(checkpoint_id)

            print(f"⚡️ CHECKPOINT VALIDATION: {checkpoint_id}")
            print("=" * 50)
            print(f"Valid: {'✅ Yes' if result['valid'] else '❌ No'}")
            print(f"Recovery Feasible: {'✅ Yes' if result['recovery_feasible'] else '❌ No'}")
            print(f"Data Integrity: {'✅ Good' if result['data_integrity'] else '❌ Issues'}")

            if result['issues']:
                print(f"\n🚨 ISSUES:")
                for issue in result['issues']:
                    print(f"  • {issue}")

            if result['warnings']:
                print(f"\n⚠️  WARNINGS:")
                for warning in result['warnings']:
                    print(f"  • {warning}")

            if result['file_checks']:
                print(f"\n📁 FILE CHECKS:")
                for file_path, check in result['file_checks'].items():
                    status = "✅" if check['exists'] and check['readable'] else "❌"
                    print(f"  {status} {file_path} ({check['size']} bytes)")

        elif command == "recover":
            if len(sys.argv) < 3:
                print("Usage: python checkpoint_recovery.py recover <checkpoint_id>")
                return

            checkpoint_id = sys.argv[2]

            print(f"🚨 CHECKPOINT RECOVERY: {checkpoint_id}")
            print("=" * 50)
            print("⚠️  This will overwrite current progress state!")
            print("⚠️  A backup will be created before recovery.")
            print()

            confirm = input("Continue with recovery? Type 'YES' to confirm: ").strip()
            if confirm != 'YES':
                print("Recovery cancelled.")
                return

            result = recovery_manager.recover_from_checkpoint(checkpoint_id)

            print(f"\n🔄 RECOVERY RESULTS:")
            print(f"Success: {'✅ Yes' if result['success'] else '❌ No'}")
            print(f"Backup Created: {'✅ Yes' if result['backup_created'] else '❌ No'}")
            print(f"State Restored: {'✅ Yes' if result['state_restored'] else '❌ No'}")
            print(f"Files Restored: {len(result['files_restored'])}")
            print(f"Files Failed: {len(result['files_failed'])}")

            if result['messages']:
                print(f"\n📝 MESSAGES:")
                for message in result['messages']:
                    print(f"  • {message}")

        elif command == "emergency":
            print("🚨 EMERGENCY RECOVERY")
            print("=" * 30)
            print("Attempting recovery from most recent valid checkpoint...")

            result = recovery_manager.emergency_recovery()

            if result['success']:
                print("✅ Emergency recovery completed successfully!")
            else:
                print(f"❌ Emergency recovery failed: {result.get('message', 'Unknown error')}")

        elif command == "rebuild":
            print("🔄 REBUILDING FROM FILES")
            print("=" * 30)
            print("Analyzing project files to reconstruct progress state...")

            result = recovery_manager.rebuild_from_files()

            print(f"Success: {'✅ Yes' if result['success'] else '❌ No'}")
            print(f"Confidence: {result['confidence']}")
            print(f"Estimated Progress: {result['estimated_progress']}%")
            print(f"Detected Phase: {result['detected_phase']}")
            print(f"Probable Task: {result['probable_task']}")
            print(f"Files Analyzed: {result['files_analyzed']}")

            if result['reconstruction_notes']:
                print(f"\n📝 RECONSTRUCTION NOTES:")
                for note in result['reconstruction_notes']:
                    print(f"  • {note}")

        elif command == "help":
            print("⚡️ CLAUDECODE CHECKPOINT RECOVERY")
            print("=" * 50)
            print()
            print("🔄 RECOVERY COMMANDS:")
            print("  list              List all available checkpoints")
            print("  validate CP001    Validate specific checkpoint")
            print("  recover CP001     Recover from specific checkpoint")
            print("  emergency         Emergency recovery from latest valid checkpoint")
            print("  rebuild           Rebuild progress state from project files")
            print()
            print("📋 EXAMPLES:")
            print("  python checkpoint_recovery.py list")
            print("  python checkpoint_recovery.py validate CP003")
            print("  python checkpoint_recovery.py recover CP003")
            print("  python checkpoint_recovery.py emergency")
            print()
            print("⚠️  IMPORTANT:")
            print("  • Always validate checkpoints before recovery")
            print("  • Recovery operations create automatic backups")
            print("  • Use emergency recovery when normal methods fail")
            print("  • Rebuild is a last resort when all checkpoints are lost")

        else:
            print(f"Unknown command: {command}")
            print("Run 'python checkpoint_recovery.py help' for available commands")

    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Command execution error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
