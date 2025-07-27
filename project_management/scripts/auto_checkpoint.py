#!/usr/bin/env python3
"""
ClaudeCode Auto-Checkpoint Daemon
Provides automatic checkpoint creation based on time intervals and activity detection.

ABOUTME: This daemon monitors ClaudeCode development activity and creates
automatic checkpoints to prevent work loss during long development sessions.
"""

import json
import os
import sys
import time
import threading
import signal
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('progress-state/auto_checkpoint.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('AutoCheckpoint')


class AutoCheckpointDaemon:
    """Automatic checkpoint creation daemon."""

    def __init__(self, project_root: str = None):
        """Initialize the auto-checkpoint daemon."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.progress_dir = self.project_root / "progress-state"
        self.state_file = self.progress_dir / "PROGRESS_STATE.json"
        self.checkpoints_dir = self.progress_dir / "checkpoints"
        self.snapshots_dir = self.progress_dir / "snapshots"

        # Daemon configuration
        self.checkpoint_interval = 30 * 60  # 30 minutes in seconds
        self.activity_threshold = 3  # Number of file changes to trigger checkpoint
        self.max_checkpoints = 50  # Maximum number of auto-checkpoints to keep
        self.running = False
        self.last_checkpoint_time = time.time()
        self.last_state_hash = None
        self.file_change_count = 0
        self.monitored_extensions = {'.py', '.md', '.json', '.yaml', '.yml', '.txt', '.js', '.ts', '.go', '.rs'}

        # Thread management
        self.checkpoint_thread = None
        self.monitor_thread = None
        self.shutdown_event = threading.Event()

        # Ensure directories exist
        self.progress_dir.mkdir(exist_ok=True)
        self.checkpoints_dir.mkdir(exist_ok=True)
        self.snapshots_dir.mkdir(exist_ok=True)

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop()

    def start(self):
        """Start the auto-checkpoint daemon."""
        if self.running:
            logger.warning("Auto-checkpoint daemon is already running")
            return

        logger.info("Starting ClaudeCode Auto-Checkpoint Daemon")
        self.running = True

        # Start checkpoint thread
        self.checkpoint_thread = threading.Thread(target=self._checkpoint_loop, daemon=True)
        self.checkpoint_thread.start()

        # Start file monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

        logger.info(f"Auto-checkpoint daemon started (interval: {self.checkpoint_interval}s)")

    def stop(self):
        """Stop the auto-checkpoint daemon."""
        if not self.running:
            return

        logger.info("Stopping auto-checkpoint daemon...")
        self.running = False
        self.shutdown_event.set()

        # Wait for threads to finish
        if self.checkpoint_thread and self.checkpoint_thread.is_alive():
            self.checkpoint_thread.join(timeout=5)
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)

        logger.info("Auto-checkpoint daemon stopped")

    def _checkpoint_loop(self):
        """Main checkpoint creation loop."""
        while self.running and not self.shutdown_event.is_set():
            try:
                current_time = time.time()
                time_since_last = current_time - self.last_checkpoint_time

                # Check if it's time for a checkpoint
                should_checkpoint = False
                checkpoint_reason = None

                if time_since_last >= self.checkpoint_interval:
                    should_checkpoint = True
                    checkpoint_reason = "TIME_BASED"
                elif self.file_change_count >= self.activity_threshold:
                    should_checkpoint = True
                    checkpoint_reason = "ACTIVITY_BASED"
                elif self._state_changed():
                    should_checkpoint = True
                    checkpoint_reason = "STATE_CHANGE"

                if should_checkpoint:
                    self._create_auto_checkpoint(checkpoint_reason)
                    self.last_checkpoint_time = current_time
                    self.file_change_count = 0

                # Sleep for 1 minute before next check
                self.shutdown_event.wait(60)

            except Exception as e:
                logger.error(f"Error in checkpoint loop: {e}")
                self.shutdown_event.wait(60)

    def _monitor_loop(self):
        """Monitor file system for changes."""
        last_check = time.time()

        while self.running and not self.shutdown_event.is_set():
            try:
                current_time = time.time()

                # Check for file modifications in the last minute
                changes = self._scan_for_changes(last_check)
                if changes:
                    self.file_change_count += len(changes)
                    logger.debug(f"Detected {len(changes)} file changes")

                last_check = current_time
                self.shutdown_event.wait(60)  # Check every minute

            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                self.shutdown_event.wait(60)

    def _scan_for_changes(self, since_time: float) -> list:
        """Scan for file changes since given time."""
        changes = []

        try:
            for file_path in self.project_root.rglob('*'):
                if (file_path.is_file() and
                    file_path.suffix in self.monitored_extensions and
                    not self._is_excluded_path(file_path) and
                    file_path.stat().st_mtime > since_time):
                    changes.append(str(file_path.relative_to(self.project_root)))
        except Exception as e:
            logger.error(f"Error scanning for changes: {e}")

        return changes

    def _is_excluded_path(self, file_path: Path) -> bool:
        """Check if path should be excluded from monitoring."""
        exclude_patterns = {
            '.git', '__pycache__', '.pytest_cache', 'node_modules',
            '.venv', 'venv', 'env', '.env', 'checkpoints', 'snapshots'
        }

        for part in file_path.parts:
            if part in exclude_patterns or part.startswith('.'):
                return True
        return False

    def _state_changed(self) -> bool:
        """Check if progress state has changed significantly."""
        try:
            if not self.state_file.exists():
                return False

            with open(self.state_file, 'r', encoding='utf-8') as f:
                current_state = f.read()

            current_hash = hashlib.md5(current_state.encode()).hexdigest()

            if self.last_state_hash is None:
                self.last_state_hash = current_hash
                return False

            if current_hash != self.last_state_hash:
                self.last_state_hash = current_hash
                return True

            return False

        except Exception as e:
            logger.error(f"Error checking state changes: {e}")
            return False

    def _create_auto_checkpoint(self, reason: str):
        """Create an automatic checkpoint."""
        try:
            # Load current progress state
            if not self.state_file.exists():
                logger.warning("Progress state file not found, skipping auto-checkpoint")
                return

            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)

            # Generate checkpoint ID
            checkpoint_count = len([f for f in self.checkpoints_dir.glob('AUTO_CP*.json')]) + 1
            checkpoint_id = f"AUTO_CP{checkpoint_count:03d}"

            # Create checkpoint data
            checkpoint = {
                "checkpoint_id": checkpoint_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": "AUTO",
                "trigger": reason,
                "description": f"Automatic checkpoint ({reason.lower().replace('_', ' ')})",
                "phase": state.get("metadata", {}).get("current_phase", 1),
                "task": state.get("current_session", {}).get("active_task", "UNKNOWN"),
                "completion_percentage": state.get("metadata", {}).get("overall_progress", 0),
                "files_modified": self._get_recently_modified_files(),
                "context_snapshot": state.get("current_session", {}).get("context_summary", ""),
                "next_actions": ["Continue with current task"],
                "auto_generated": True,
                "file_change_count": self.file_change_count,
                "validation_status": "PENDING"
            }

            # Save checkpoint to file
            timestamp_str = datetime.now().strftime('%Y%m%d_%H%M')
            checkpoint_file = self.checkpoints_dir / f"{checkpoint_id}_{timestamp_str}_{reason.lower()}.json"

            checkpoint_data = {
                "checkpoint": checkpoint,
                "full_state": state,
                "system_info": {
                    "python_version": sys.version,
                    "platform": sys.platform,
                    "daemon_version": "1.0"
                }
            }

            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)

            # Update state with checkpoint info
            if "checkpoints" not in state:
                state["checkpoints"] = []
            state["checkpoints"].append(checkpoint)

            # Update automation metadata
            if "automation" not in state:
                state["automation"] = {}
            if "auto_checkpoint" not in state["automation"]:
                state["automation"]["auto_checkpoint"] = {}

            state["automation"]["auto_checkpoint"]["last_auto_checkpoint"] = checkpoint["timestamp"]
            state["automation"]["auto_checkpoint"]["total_auto_checkpoints"] = checkpoint_count

            # Update recovery info
            if "recovery" not in state:
                state["recovery"] = {}
            state["recovery"]["last_known_good_state"] = checkpoint_id
            state["recovery"]["rollback_available"] = True

            # Save updated state
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

            logger.info(f"Auto-checkpoint {checkpoint_id} created successfully ({reason})")

            # Cleanup old checkpoints
            self._cleanup_old_checkpoints()

        except Exception as e:
            logger.error(f"Failed to create auto-checkpoint: {e}")

    def _get_recently_modified_files(self) -> list:
        """Get list of recently modified files."""
        recent_files = []
        cutoff_time = time.time() - 3600  # Last hour

        try:
            for file_path in self.project_root.rglob('*'):
                if (file_path.is_file() and
                    file_path.suffix in self.monitored_extensions and
                    not self._is_excluded_path(file_path) and
                    file_path.stat().st_mtime > cutoff_time):
                    recent_files.append(str(file_path.relative_to(self.project_root)))
        except Exception as e:
            logger.error(f"Error getting recent files: {e}")

        return recent_files[:20]  # Limit to 20 most recent

    def _cleanup_old_checkpoints(self):
        """Clean up old auto-checkpoints to prevent disk space issues."""
        try:
            auto_checkpoints = list(self.checkpoints_dir.glob('AUTO_CP*.json'))
            auto_checkpoints.sort(key=lambda x: x.stat().st_mtime)

            if len(auto_checkpoints) > self.max_checkpoints:
                old_checkpoints = auto_checkpoints[:-self.max_checkpoints]
                for checkpoint_file in old_checkpoints:
                    checkpoint_file.unlink()
                    logger.debug(f"Cleaned up old checkpoint: {checkpoint_file.name}")

                logger.info(f"Cleaned up {len(old_checkpoints)} old auto-checkpoints")

        except Exception as e:
            logger.error(f"Error during checkpoint cleanup: {e}")

    def force_checkpoint(self, description: str = None):
        """Force creation of an immediate checkpoint."""
        reason = "MANUAL_TRIGGER"
        logger.info("Force creating checkpoint...")
        self._create_auto_checkpoint(reason)

    def get_status(self) -> dict:
        """Get current daemon status."""
        return {
            "running": self.running,
            "last_checkpoint": datetime.fromtimestamp(self.last_checkpoint_time).isoformat(),
            "file_changes": self.file_change_count,
            "checkpoint_interval": self.checkpoint_interval,
            "total_checkpoints": len(list(self.checkpoints_dir.glob('AUTO_CP*.json')))
        }

    def run_daemon(self):
        """Run the daemon in foreground mode."""
        try:
            self.start()
            logger.info("Auto-checkpoint daemon running. Press Ctrl+C to stop.")

            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            self.stop()


def main():
    """Main entry point for auto-checkpoint daemon."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        daemon = AutoCheckpointDaemon()

        if command == "start":
            daemon.run_daemon()
        elif command == "status":
            status = daemon.get_status()
            print("⚡️ AUTO-CHECKPOINT DAEMON STATUS")
            print("=" * 40)
            print(f"Running: {'✅ Yes' if status['running'] else '❌ No'}")
            print(f"Last Checkpoint: {status['last_checkpoint']}")
            print(f"File Changes: {status['file_changes']}")
            print(f"Interval: {status['checkpoint_interval']}s")
            print(f"Total Auto-Checkpoints: {status['total_checkpoints']}")
        elif command == "checkpoint":
            daemon.force_checkpoint("Manual force checkpoint")
            print("✅ Force checkpoint created")
        elif command == "help":
            print("⚡️ CLAUDECODE AUTO-CHECKPOINT DAEMON")
            print("=" * 50)
            print("Commands:")
            print("  python auto_checkpoint.py start      # Start daemon")
            print("  python auto_checkpoint.py status     # Check status")
            print("  python auto_checkpoint.py checkpoint # Force checkpoint")
            print("  python auto_checkpoint.py help       # Show this help")
            print("\nThe daemon automatically creates checkpoints every 30 minutes")
            print("or when significant file changes are detected.")
        else:
            print(f"Unknown command: {command}")
            print("Run 'python auto_checkpoint.py help' for usage information")
    else:
        print("Usage: python auto_checkpoint.py <command>")
        print("Run 'python auto_checkpoint.py help' for more information")


if __name__ == "__main__":
    main()
