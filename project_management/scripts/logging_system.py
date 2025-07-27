#!/usr/bin/env python3
"""
ClaudeCode Structured Logging System
====================================

Comprehensive logging system for tracking AI development sessions, decisions,
progress, and system interactions. Provides structured logging with multiple
output formats and advanced analytics capabilities.

Usage:
    from logging_system import ClaudeLogger, SessionTracker, DecisionLogger

    logger = ClaudeLogger("my_project")
    session = SessionTracker(logger)
    decisions = DecisionLogger(logger)

    session.start_session("Feature implementation")
    decisions.log_decision("Use React for frontend", rationale="Team familiarity")
    session.end_session(success=True)

Features:
    - Structured session tracking
    - Decision logging with rationale
    - Progress monitoring
    - Error tracking and analysis
    - Performance metrics
    - Multiple output formats (JSON, Markdown, CSV)
    - Automatic log rotation and archival
    - Analytics and reporting
"""

import json
import logging
import os
import time
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import gzip
import shutil


class LogLevel(Enum):
    """Log severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class EventType(Enum):
    """Types of events that can be logged."""
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    TASK_START = "task_start"
    TASK_COMPLETE = "task_complete"
    DECISION_MADE = "decision_made"
    ERROR_OCCURRED = "error_occurred"
    PROGRESS_UPDATE = "progress_update"
    CONTEXT_CHANGE = "context_change"
    WORKFLOW_CHANGE = "workflow_change"
    QUALITY_GATE = "quality_gate"
    PERFORMANCE_METRIC = "performance_metric"
    USER_INTERACTION = "user_interaction"
    AI_RESPONSE = "ai_response"


@dataclass
class LogEntry:
    """Structured log entry with comprehensive metadata."""
    timestamp: str
    event_type: EventType
    level: LogLevel
    session_id: str
    message: str
    data: Dict[str, Any]
    source: str
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    workflow_id: Optional[str] = None
    task_id: Optional[str] = None
    duration_ms: Optional[int] = None
    tags: Optional[List[str]] = None
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        result['event_type'] = self.event_type.value
        result['level'] = self.level.value
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)


class LogStorage:
    """Handles log storage, rotation, and archival."""

    def __init__(self, log_dir: Path, max_file_size_mb: int = 10,
                 max_files: int = 50, compress_old: bool = True):
        self.log_dir = log_dir
        self.max_file_size = max_file_size_mb * 1024 * 1024
        self.max_files = max_files
        self.compress_old = compress_old
        self.current_file = None
        self.current_size = 0
        self._lock = threading.Lock()

        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Initialize current log file
        self._rotate_if_needed()

    def write_entry(self, entry: LogEntry) -> None:
        """Write log entry to storage."""
        with self._lock:
            self._rotate_if_needed()

            if self.current_file:
                entry_json = entry.to_json() + '\n'
                self.current_file.write(entry_json)
                self.current_file.flush()
                self.current_size += len(entry_json.encode('utf-8'))

    def _rotate_if_needed(self) -> None:
        """Rotate log file if size limit exceeded."""
        if (self.current_file is None or
            self.current_size >= self.max_file_size):

            # Close current file
            if self.current_file:
                self.current_file.close()

            # Generate new filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"claude_log_{timestamp}.jsonl"
            filepath = self.log_dir / filename

            # Open new file
            self.current_file = open(filepath, 'w')
            self.current_size = 0

            # Clean up old files
            self._cleanup_old_files()

    def _cleanup_old_files(self) -> None:
        """Remove old log files and compress if configured."""
        log_files = list(self.log_dir.glob("claude_log_*.jsonl"))
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        # Compress old files if enabled
        if self.compress_old:
            for log_file in log_files[1:]:  # Skip current file
                compressed_path = log_file.with_suffix('.jsonl.gz')
                if not compressed_path.exists():
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(compressed_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    log_file.unlink()  # Remove original

        # Remove excess files
        all_files = (list(self.log_dir.glob("claude_log_*.jsonl")) +
                    list(self.log_dir.glob("claude_log_*.jsonl.gz")))
        all_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        for old_file in all_files[self.max_files:]:
            old_file.unlink()

    def close(self) -> None:
        """Close current log file."""
        with self._lock:
            if self.current_file:
                self.current_file.close()
                self.current_file = None


class ClaudeLogger:
    """Main logging interface for ClaudeCode system."""

    def __init__(self, project_name: str, log_dir: Optional[Path] = None,
                 user_id: Optional[str] = None):
        self.project_name = project_name
        self.project_id = str(uuid.uuid4())
        self.user_id = user_id or "default_user"

        # Set up log directory
        if log_dir is None:
            log_dir = Path.cwd() / "logs" / project_name
        self.log_dir = log_dir

        # Initialize storage
        self.storage = LogStorage(log_dir)

        # Session tracking
        self.current_session_id = None
        self.session_start_time = None

        # Statistics
        self.stats = defaultdict(int)
        self._start_time = time.time()

    def log(self, event_type: EventType, message: str, level: LogLevel = LogLevel.INFO,
            data: Optional[Dict[str, Any]] = None, source: str = "claude_code",
            workflow_id: Optional[str] = None, task_id: Optional[str] = None,
            duration_ms: Optional[int] = None, tags: Optional[List[str]] = None,
            correlation_id: Optional[str] = None) -> None:
        """Log a structured event."""

        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            level=level,
            session_id=self.current_session_id or "no_session",
            message=message,
            data=data or {},
            source=source,
            user_id=self.user_id,
            project_id=self.project_id,
            workflow_id=workflow_id,
            task_id=task_id,
            duration_ms=duration_ms,
            tags=tags,
            correlation_id=correlation_id
        )

        # Store the entry
        self.storage.write_entry(entry)

        # Update statistics
        self.stats[f"events_{event_type.value}"] += 1
        self.stats[f"level_{level.value}"] += 1

        # Also log to console for immediate visibility
        self._console_log(entry)

    def _console_log(self, entry: LogEntry) -> None:
        """Log to console with appropriate formatting."""
        timestamp = datetime.fromisoformat(entry.timestamp).strftime("%H:%M:%S")
        level_icons = {
            LogLevel.DEBUG: "🔍",
            LogLevel.INFO: "ℹ️",
            LogLevel.WARNING: "⚠️",
            LogLevel.ERROR: "❌",
            LogLevel.CRITICAL: "🚨"
        }

        icon = level_icons.get(entry.level, "📝")
        session_short = entry.session_id[:8] if entry.session_id != "no_session" else "--------"

        print(f"{timestamp} {icon} [{session_short}] {entry.message}")

        if entry.level in [LogLevel.ERROR, LogLevel.CRITICAL] and entry.data:
            print(f"    Data: {json.dumps(entry.data, indent=2)}")

    def get_stats(self) -> Dict[str, Any]:
        """Get logging statistics."""
        runtime = time.time() - self._start_time
        return {
            "project_name": self.project_name,
            "project_id": self.project_id,
            "runtime_seconds": runtime,
            "current_session": self.current_session_id,
            "stats": dict(self.stats)
        }

    def close(self) -> None:
        """Close logger and clean up resources."""
        if self.current_session_id:
            self.log(EventType.SESSION_END, "Logger shutting down",
                    level=LogLevel.INFO)
        self.storage.close()


class SessionTracker:
    """Tracks development sessions with detailed metadata."""

    def __init__(self, logger: ClaudeLogger):
        self.logger = logger
        self.session_data = {}
        self.task_stack = []

    def start_session(self, objective: str, context: Optional[Dict[str, Any]] = None,
                     estimated_duration_minutes: Optional[int] = None) -> str:
        """Start a new development session."""
        session_id = str(uuid.uuid4())

        self.logger.current_session_id = session_id
        self.logger.session_start_time = time.time()

        session_data = {
            "objective": objective,
            "context": context or {},
            "estimated_duration_minutes": estimated_duration_minutes,
            "tasks_planned": [],
            "tasks_completed": [],
            "decisions_made": [],
            "challenges_encountered": []
        }

        self.session_data[session_id] = session_data

        self.logger.log(
            EventType.SESSION_START,
            f"Started session: {objective}",
            data=session_data
        )

        return session_id

    def end_session(self, success: bool = True, summary: Optional[str] = None,
                   learnings: Optional[List[str]] = None) -> Dict[str, Any]:
        """End the current development session."""
        if not self.logger.current_session_id:
            raise ValueError("No active session to end")

        session_id = self.logger.current_session_id
        duration = time.time() - self.logger.session_start_time

        session_summary = {
            "success": success,
            "summary": summary,
            "learnings": learnings or [],
            "duration_seconds": duration,
            "tasks_planned": len(self.session_data[session_id]["tasks_planned"]),
            "tasks_completed": len(self.session_data[session_id]["tasks_completed"]),
            "decisions_made": len(self.session_data[session_id]["decisions_made"])
        }

        self.logger.log(
            EventType.SESSION_END,
            f"Ended session: {'Success' if success else 'Incomplete'}",
            data=session_summary,
            duration_ms=int(duration * 1000)
        )

        # Reset session tracking
        result = self.session_data[session_id].copy()
        result.update(session_summary)

        self.logger.current_session_id = None
        self.logger.session_start_time = None

        return result

    def start_task(self, task_name: str, task_type: str = "development",
                  estimated_duration_minutes: Optional[int] = None) -> str:
        """Start a new task within the current session."""
        task_id = str(uuid.uuid4())

        task_data = {
            "task_name": task_name,
            "task_type": task_type,
            "estimated_duration_minutes": estimated_duration_minutes,
            "start_time": time.time()
        }

        self.task_stack.append((task_id, task_data))

        if self.logger.current_session_id:
            self.session_data[self.logger.current_session_id]["tasks_planned"].append(task_data)

        self.logger.log(
            EventType.TASK_START,
            f"Started task: {task_name}",
            data=task_data,
            task_id=task_id
        )

        return task_id

    def complete_task(self, task_id: str, success: bool = True,
                     notes: Optional[str] = None) -> None:
        """Mark a task as completed."""
        # Find task in stack
        task_index = None
        for i, (tid, _) in enumerate(self.task_stack):
            if tid == task_id:
                task_index = i
                break

        if task_index is None:
            self.logger.log(EventType.ERROR, f"Task not found: {task_id}")
            return

        _, task_data = self.task_stack.pop(task_index)
        duration = time.time() - task_data["start_time"]

        completion_data = {
            "success": success,
            "notes": notes,
            "actual_duration_seconds": duration,
            "original_estimate_minutes": task_data.get("estimated_duration_minutes")
        }
        completion_data.update(task_data)

        if self.logger.current_session_id:
            self.session_data[self.logger.current_session_id]["tasks_completed"].append(completion_data)

        self.logger.log(
            EventType.TASK_COMPLETE,
            f"Completed task: {task_data['task_name']} ({'Success' if success else 'Failed'})",
            data=completion_data,
            task_id=task_id,
            duration_ms=int(duration * 1000)
        )

    def update_progress(self, task_id: str, progress_percentage: int,
                       details: Optional[str] = None) -> None:
        """Update progress on a task."""
        progress_data = {
            "progress_percentage": progress_percentage,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }

        self.logger.log(
            EventType.PROGRESS_UPDATE,
            f"Progress update: {progress_percentage}%",
            data=progress_data,
            task_id=task_id
        )


class DecisionLogger:
    """Logs development decisions with rationale and alternatives."""

    def __init__(self, logger: ClaudeLogger):
        self.logger = logger
        self.decisions = []

    def log_decision(self, decision: str, rationale: str,
                    alternatives: Optional[List[str]] = None,
                    impact: str = "medium", reversible: bool = True,
                    stakeholders: Optional[List[str]] = None,
                    references: Optional[List[str]] = None) -> str:
        """Log a development decision with comprehensive context."""
        decision_id = str(uuid.uuid4())

        decision_data = {
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "alternatives": alternatives or [],
            "impact": impact,  # low, medium, high, critical
            "reversible": reversible,
            "stakeholders": stakeholders or [],
            "references": references or [],
            "timestamp": datetime.now().isoformat()
        }

        self.decisions.append(decision_data)

        if self.logger.current_session_id:
            session_data = self.logger.storage
            # Add to session decisions if session is active

        self.logger.log(
            EventType.DECISION_MADE,
            f"Decision: {decision}",
            data=decision_data,
            tags=["decision", impact]
        )

        return decision_id

    def revise_decision(self, decision_id: str, new_decision: str,
                       revision_rationale: str) -> str:
        """Revise a previous decision."""
        # Find original decision
        original = None
        for decision in self.decisions:
            if decision["decision_id"] == decision_id:
                original = decision
                break

        if not original:
            self.logger.log(EventType.ERROR, f"Decision not found for revision: {decision_id}")
            return decision_id

        revision_data = {
            "original_decision_id": decision_id,
            "original_decision": original["decision"],
            "new_decision": new_decision,
            "revision_rationale": revision_rationale,
            "revision_timestamp": datetime.now().isoformat()
        }

        self.logger.log(
            EventType.DECISION_MADE,
            f"Decision revised: {new_decision}",
            data=revision_data,
            tags=["decision", "revision"]
        )

        return self.log_decision(
            new_decision,
            f"Revision of previous decision: {revision_rationale}",
            impact=original["impact"]
        )


class PerformanceTracker:
    """Tracks performance metrics and system health."""

    def __init__(self, logger: ClaudeLogger):
        self.logger = logger
        self.metrics = defaultdict(list)
        self.thresholds = {
            "response_time_ms": 5000,
            "memory_usage_mb": 1024,
            "error_rate_percent": 5.0
        }

    def record_metric(self, metric_name: str, value: float,
                     unit: str = "count", context: Optional[Dict] = None) -> None:
        """Record a performance metric."""
        metric_data = {
            "metric_name": metric_name,
            "value": value,
            "unit": unit,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }

        self.metrics[metric_name].append(metric_data)

        # Check against thresholds
        if metric_name in self.thresholds:
            threshold = self.thresholds[metric_name]
            if value > threshold:
                self.logger.log(
                    EventType.PERFORMANCE_METRIC,
                    f"Performance threshold exceeded: {metric_name} = {value} > {threshold}",
                    level=LogLevel.WARNING,
                    data=metric_data,
                    tags=["performance", "threshold_exceeded"]
                )
            else:
                self.logger.log(
                    EventType.PERFORMANCE_METRIC,
                    f"Performance metric recorded: {metric_name} = {value}",
                    data=metric_data,
                    tags=["performance"]
                )
        else:
            self.logger.log(
                EventType.PERFORMANCE_METRIC,
                f"Metric recorded: {metric_name} = {value}",
                data=metric_data,
                tags=["performance"]
            )

    def get_metric_summary(self, metric_name: str,
                          time_window_hours: Optional[int] = None) -> Dict[str, Any]:
        """Get summary statistics for a metric."""
        if metric_name not in self.metrics:
            return {}

        metrics_data = self.metrics[metric_name]

        # Filter by time window if specified
        if time_window_hours:
            cutoff = datetime.now() - timedelta(hours=time_window_hours)
            metrics_data = [
                m for m in metrics_data
                if datetime.fromisoformat(m["timestamp"]) > cutoff
            ]

        if not metrics_data:
            return {}

        values = [m["value"] for m in metrics_data]

        return {
            "metric_name": metric_name,
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "latest": values[-1],
            "time_window_hours": time_window_hours
        }


class LogAnalyzer:
    """Analyzes log data to provide insights and reports."""

    def __init__(self, log_dir: Path):
        self.log_dir = log_dir

    def analyze_session_patterns(self) -> Dict[str, Any]:
        """Analyze session patterns and productivity metrics."""
        log_files = list(self.log_dir.glob("claude_log_*.jsonl*"))

        sessions = []
        tasks = []
        decisions = []

        for log_file in log_files:
            for entry_data in self._read_log_file(log_file):
                if entry_data["event_type"] == "session_start":
                    sessions.append(entry_data)
                elif entry_data["event_type"] == "task_complete":
                    tasks.append(entry_data)
                elif entry_data["event_type"] == "decision_made":
                    decisions.append(entry_data)

        return {
            "total_sessions": len(sessions),
            "total_tasks": len(tasks),
            "total_decisions": len(decisions),
            "avg_tasks_per_session": len(tasks) / max(len(sessions), 1),
            "avg_decisions_per_session": len(decisions) / max(len(sessions), 1),
            "task_success_rate": sum(1 for t in tasks if t["data"].get("success", True)) / max(len(tasks), 1)
        }

    def _read_log_file(self, log_file: Path):
        """Read and parse log file entries."""
        try:
            if log_file.suffix == '.gz':
                with gzip.open(log_file, 'rt') as f:
                    for line in f:
                        if line.strip():
                            yield json.loads(line)
            else:
                with open(log_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            yield json.loads(line)
        except Exception as e:
            print(f"Error reading log file {log_file}: {e}")

    def generate_daily_report(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Generate daily activity report."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # This would analyze logs for specific date
        # Implementation would filter logs by timestamp
        return {
            "date": date,
            "sessions_count": 0,
            "tasks_completed": 0,
            "decisions_made": 0,
            "errors_encountered": 0,
            "total_development_time_hours": 0
        }


# Convenience functions for easy usage
def get_default_logger(project_name: str) -> ClaudeLogger:
    """Get a default configured logger for a project."""
    return ClaudeLogger(project_name)

def create_session_tracker(project_name: str) -> Tuple[ClaudeLogger, SessionTracker]:
    """Create logger and session tracker for a project."""
    logger = get_default_logger(project_name)
    tracker = SessionTracker(logger)
    return logger, tracker

def create_full_logging_suite(project_name: str) -> Tuple[ClaudeLogger, SessionTracker, DecisionLogger, PerformanceTracker]:
    """Create complete logging suite for a project."""
    logger = get_default_logger(project_name)
    session_tracker = SessionTracker(logger)
    decision_logger = DecisionLogger(logger)
    performance_tracker = PerformanceTracker(logger)

    return logger, session_tracker, decision_logger, performance_tracker


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    logger, session, decisions, performance = create_full_logging_suite("test_project")

    # Start a session
    session_id = session.start_session("Implement user authentication",
                                     estimated_duration_minutes=120)

    # Start a task
    task_id = session.start_task("Design user model", "architecture")

    # Log a decision
    decisions.log_decision(
        "Use JWT for authentication",
        "Provides stateless authentication suitable for microservices",
        alternatives=["Session-based auth", "OAuth only"],
        impact="high"
    )

    # Record performance metric
    performance.record_metric("api_response_time", 150, "milliseconds")

    # Complete task
    session.complete_task(task_id, success=True, notes="User model designed and reviewed")

    # End session
    summary = session.end_session(success=True,
                                summary="Successfully implemented authentication system",
                                learnings=["JWT implementation is straightforward",
                                         "Need better error handling for token expiry"])

    print("Session completed:", summary)
    print("Logger stats:", logger.get_stats())

    # Close logger
    logger.close()
