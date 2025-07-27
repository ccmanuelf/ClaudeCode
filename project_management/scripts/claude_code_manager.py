#!/usr/bin/env python3
"""
ClaudeCode System Manager
========================

Comprehensive system management script for the ClaudeCode AI Engineering Platform.
Provides unified interface for system initialization, validation, monitoring,
and maintenance operations.

Usage:
    python claude_code_manager.py status
    python claude_code_manager.py validate --fix
    python claude_code_manager.py init-project --name "my-project" --type "web-app"
    python claude_code_manager.py start-monitoring
    python claude_code_manager.py health-check
    python claude_code_manager.py generate-report

Features:
    - System health monitoring and validation
    - Project initialization and management
    - Performance monitoring coordination
    - Configuration validation and auto-repair
    - Comprehensive reporting and analytics
    - Session management and recovery
    - Automated maintenance tasks
    - Integration status checking
"""

import argparse
import json
import os
import subprocess
import sys
import time
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import threading
import signal

# Import our custom modules
try:
    from init_project import ProjectInitializer
    from validate_config import ConfigValidator
    from logging_system import ClaudeLogger, SessionTracker, DecisionLogger, create_full_logging_suite
    from performance_monitor import PerformanceMonitor
except ImportError as e:
    print(f"Warning: Could not import all modules: {e}")
    print("Some features may not be available.")


class ClaudeCodeManager:
    """Main system manager for ClaudeCode AI Engineering Platform."""

    def __init__(self, claude_code_root: Optional[Path] = None):
        self.root = Path(claude_code_root or Path(__file__).parent.parent).resolve()
        self.config_file = self.root / "config.yaml"
        self.scripts_dir = self.root / "scripts"
        self.logs_dir = self.root / "logs"

        # System state
        self.config_data = None
        self.system_health = {}
        self.active_monitors = {}
        self.logger = None

        # Ensure logs directory exists
        self.logs_dir.mkdir(exist_ok=True)

        # Initialize logging
        self._init_logging()

        # Load configuration
        self._load_config()

    def _init_logging(self) -> None:
        """Initialize system logging."""
        try:
            self.logger = ClaudeLogger("claude_code_system", self.logs_dir / "system")
            self.logger.log_info("ClaudeCode Manager initialized")
        except Exception as e:
            print(f"Warning: Could not initialize logging: {e}")

    def _load_config(self) -> None:
        """Load ClaudeCode configuration."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config_data = yaml.safe_load(f)
            else:
                print(f"Warning: Configuration file not found: {self.config_file}")
                self.config_data = {}
        except Exception as e:
            print(f"Error loading configuration: {e}")
            self.config_data = {}

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        status = {
            "timestamp": datetime.now().isoformat(),
            "claude_code_root": str(self.root),
            "config_loaded": self.config_data is not None,
            "version": self.config_data.get("system", {}).get("version", "unknown"),
            "mode": self.config_data.get("system", {}).get("mode", "lite"),
        }

        # Check core components
        status["components"] = self._check_components()

        # Check directory structure
        status["directories"] = self._check_directories()

        # Check dependencies
        status["dependencies"] = self._check_dependencies()

        # Performance status
        status["performance"] = self._get_performance_status()

        # Overall health
        status["health"] = self._calculate_overall_health(status)

        return status

    def _check_components(self) -> Dict[str, bool]:
        """Check if core components are available."""
        components = {
            "config_file": self.config_file.exists(),
            "scripts_directory": self.scripts_dir.exists(),
            "logs_directory": self.logs_dir.exists(),
        }

        # Check for key script files
        key_scripts = [
            "init_project.py",
            "validate_config.py",
            "logging_system.py",
            "performance_monitor.py"
        ]

        for script in key_scripts:
            components[f"script_{script}"] = (self.scripts_dir / script).exists()

        # Check configuration sections
        if self.config_data:
            required_sections = ["persona", "workflows", "behaviors", "guardrails"]
            for section in required_sections:
                components[f"config_{section}"] = section in self.config_data

        return components

    def _check_directories(self) -> Dict[str, Dict[str, Any]]:
        """Check directory structure and contents."""
        directories = {}

        expected_dirs = [
            "agent-config",
            "agent-config/persona",
            "agent-config/prompts",
            "agent-config/guardrails",
            "agent-config/behaviors",
            "agent-config/workflows",
            "agent-config/templates",
            "features",
            "logs",
            "tasks",
            "scripts"
        ]

        for dir_path in expected_dirs:
            full_path = self.root / dir_path
            directories[dir_path] = {
                "exists": full_path.exists(),
                "is_directory": full_path.is_dir() if full_path.exists() else False,
                "file_count": len(list(full_path.glob("*"))) if full_path.exists() and full_path.is_dir() else 0
            }

        return directories

    def _check_dependencies(self) -> Dict[str, Dict[str, Any]]:
        """Check system dependencies."""
        dependencies = {}

        # Python
        try:
            python_version = subprocess.run([sys.executable, "--version"],
                                          capture_output=True, text=True, check=True)
            dependencies["python"] = {
                "available": True,
                "version": python_version.stdout.strip(),
                "path": sys.executable
            }
        except Exception as e:
            dependencies["python"] = {"available": False, "error": str(e)}

        # Git
        try:
            git_version = subprocess.run(["git", "--version"],
                                       capture_output=True, text=True, check=True)
            dependencies["git"] = {
                "available": True,
                "version": git_version.stdout.strip()
            }
        except Exception as e:
            dependencies["git"] = {"available": False, "error": str(e)}

        # UV package manager
        try:
            uv_version = subprocess.run(["uv", "--version"],
                                      capture_output=True, text=True, check=True)
            dependencies["uv"] = {
                "available": True,
                "version": uv_version.stdout.strip()
            }
        except Exception as e:
            dependencies["uv"] = {"available": False, "error": str(e)}

        # Optional dependencies
        optional_deps = ["gh", "pre-commit", "docker"]
        for dep in optional_deps:
            try:
                result = subprocess.run([dep, "--version"],
                                      capture_output=True, text=True, check=True)
                dependencies[dep] = {
                    "available": True,
                    "version": result.stdout.strip(),
                    "optional": True
                }
            except Exception:
                dependencies[dep] = {
                    "available": False,
                    "optional": True
                }

        return dependencies

    def _get_performance_status(self) -> Dict[str, Any]:
        """Get current performance status."""
        try:
            import psutil

            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else None,
                "process_count": len(psutil.pids())
            }
        except Exception:
            return {"error": "Performance monitoring not available"}

    def _calculate_overall_health(self, status: Dict[str, Any]) -> str:
        """Calculate overall system health."""
        issues = []

        # Check components
        components = status.get("components", {})
        critical_components = ["config_file", "scripts_directory"]

        for component in critical_components:
            if not components.get(component, False):
                issues.append(f"Missing critical component: {component}")

        # Check dependencies
        dependencies = status.get("dependencies", {})
        required_deps = ["python", "git", "uv"]

        for dep in required_deps:
            if not dependencies.get(dep, {}).get("available", False):
                issues.append(f"Missing required dependency: {dep}")

        # Check performance
        performance = status.get("performance", {})
        if performance.get("cpu_percent", 0) > 90:
            issues.append("High CPU usage")
        if performance.get("memory_percent", 0) > 90:
            issues.append("High memory usage")
        if performance.get("disk_percent", 0) > 95:
            issues.append("Low disk space")

        # Determine health level
        if not issues:
            return "healthy"
        elif len(issues) <= 2:
            return "warning"
        else:
            return "critical"

    def validate_system(self, auto_fix: bool = False) -> Tuple[bool, List[str]]:
        """Validate system configuration and integrity."""
        print("🔍 Validating ClaudeCode system...")

        try:
            validator = ConfigValidator(self.root)
            success = validator.validate_all()

            if auto_fix and not success:
                print("🔧 Attempting automatic fixes...")
                fixed_count = validator.auto_fix_issues()
                if fixed_count > 0:
                    print(f"✅ Fixed {fixed_count} issues automatically")
                    # Re-validate after fixes
                    success = validator.validate_all()

            # Collect validation messages
            messages = []
            for error in validator.errors:
                level_icon = {"critical": "❌", "error": "🔴", "warning": "⚠️", "info": "ℹ️"}
                icon = level_icon.get(error.severity, "📝")
                messages.append(f"{icon} {error.message}")

            return success, messages

        except Exception as e:
            return False, [f"Validation failed: {str(e)}"]

    def initialize_project(self, project_name: str, project_type: str = "web-app",
                          target_dir: Optional[Path] = None,
                          create_github: bool = False) -> bool:
        """Initialize a new project with ClaudeCode integration."""
        try:
            initializer = ProjectInitializer()

            config = {
                "name": project_name,
                "type": project_type,
                "target_dir": target_dir or Path.cwd() / project_name,
                "create_github": create_github
            }

            print(f"🚀 Initializing project '{project_name}'...")
            success = initializer.run_full_initialization(config)

            if success:
                print(f"✅ Project '{project_name}' initialized successfully!")
                if self.logger:
                    self.logger.log_info(f"Project initialized: {project_name}")
                return True
            else:
                print(f"❌ Project initialization failed")
                return False

        except Exception as e:
            print(f"❌ Error initializing project: {e}")
            return False

    def start_monitoring(self, project_name: Optional[str] = None) -> bool:
        """Start performance monitoring."""
        try:
            if not project_name:
                project_name = "claude_code_system"

            print(f"📊 Starting monitoring for {project_name}...")

            monitor = PerformanceMonitor(project_name, self.logs_dir / "performance")
            monitor.start_monitoring()

            self.active_monitors[project_name] = monitor

            print("✅ Monitoring started successfully")
            if self.logger:
                self.logger.log_info(f"Monitoring started: {project_name}")

            return True

        except Exception as e:
            print(f"❌ Error starting monitoring: {e}")
            return False

    def stop_monitoring(self, project_name: Optional[str] = None) -> bool:
        """Stop performance monitoring."""
        try:
            if project_name and project_name in self.active_monitors:
                monitor = self.active_monitors[project_name]
                monitor.stop_monitoring()
                del self.active_monitors[project_name]
                print(f"⏹️ Stopped monitoring for {project_name}")
            else:
                # Stop all monitors
                for name, monitor in self.active_monitors.items():
                    monitor.stop_monitoring()
                    print(f"⏹️ Stopped monitoring for {name}")
                self.active_monitors.clear()

            return True

        except Exception as e:
            print(f"❌ Error stopping monitoring: {e}")
            return False

    def health_check(self) -> bool:
        """Perform comprehensive health check."""
        print("🏥 Performing health check...")

        status = self.get_system_status()
        health = status["health"]

        print(f"\n📊 System Health: {health.upper()}")
        print(f"Version: {status['version']}")
        print(f"Mode: {status['mode']}")

        # Component status
        print("\n🔧 Components:")
        components = status["components"]
        for component, available in components.items():
            icon = "✅" if available else "❌"
            print(f"  {icon} {component}")

        # Dependencies
        print("\n📦 Dependencies:")
        dependencies = status["dependencies"]
        for dep_name, dep_info in dependencies.items():
            if dep_info.get("available", False):
                version = dep_info.get("version", "unknown")
                optional = " (optional)" if dep_info.get("optional", False) else ""
                print(f"  ✅ {dep_name}: {version}{optional}")
            else:
                optional = " (optional)" if dep_info.get("optional", False) else ""
                print(f"  ❌ {dep_name}: Not available{optional}")

        # Performance
        print("\n⚡ Performance:")
        performance = status["performance"]
        if "error" not in performance:
            print(f"  CPU: {performance.get('cpu_percent', 0):.1f}%")
            print(f"  Memory: {performance.get('memory_percent', 0):.1f}%")
            print(f"  Disk: {performance.get('disk_percent', 0):.1f}%")
        else:
            print(f"  ❌ {performance['error']}")

        return health in ["healthy", "warning"]

    def generate_report(self, output_file: Optional[Path] = None) -> Dict[str, Any]:
        """Generate comprehensive system report."""
        print("📄 Generating system report...")

        report = {
            "report_type": "claude_code_system_report",
            "generated_at": datetime.now().isoformat(),
            "system_status": self.get_system_status(),
            "validation_results": {},
            "recent_activities": {},
            "recommendations": []
        }

        # Run validation
        validation_success, validation_messages = self.validate_system()
        report["validation_results"] = {
            "success": validation_success,
            "messages": validation_messages
        }

        # Get recent log activities (if logging is available)
        try:
            log_files = list(self.logs_dir.glob("**/*.jsonl"))
            report["recent_activities"]["log_files_count"] = len(log_files)
            report["recent_activities"]["logs_directory_size"] = sum(
                f.stat().st_size for f in log_files if f.exists()
            )
        except Exception:
            report["recent_activities"]["error"] = "Could not access log files"

        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(report)

        # Save report if output file specified
        if output_file:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"📁 Report saved to: {output_file}")

        return report

    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate system improvement recommendations."""
        recommendations = []

        status = report["system_status"]

        # Health-based recommendations
        if status["health"] == "critical":
            recommendations.append("System health is critical. Address missing dependencies and components immediately.")
        elif status["health"] == "warning":
            recommendations.append("System health needs attention. Review and fix identified issues.")

        # Component recommendations
        components = status.get("components", {})
        missing_components = [name for name, available in components.items() if not available]
        if missing_components:
            recommendations.append(f"Missing components detected: {', '.join(missing_components)}. Run validation with --fix to auto-repair.")

        # Dependency recommendations
        dependencies = status.get("dependencies", {})
        missing_required = []
        for dep_name, dep_info in dependencies.items():
            if not dep_info.get("optional", False) and not dep_info.get("available", False):
                missing_required.append(dep_name)

        if missing_required:
            recommendations.append(f"Install missing required dependencies: {', '.join(missing_required)}")

        # Performance recommendations
        performance = status.get("performance", {})
        if performance.get("cpu_percent", 0) > 80:
            recommendations.append("High CPU usage detected. Consider optimizing resource-intensive operations.")
        if performance.get("memory_percent", 0) > 80:
            recommendations.append("High memory usage detected. Monitor for memory leaks.")
        if performance.get("disk_percent", 0) > 90:
            recommendations.append("Low disk space. Clean up old logs and temporary files.")

        # Validation recommendations
        if not report["validation_results"]["success"]:
            recommendations.append("Configuration validation failed. Run 'claude_code_manager.py validate --fix' to repair issues.")

        # Usage recommendations
        if not any(self.active_monitors):
            recommendations.append("No performance monitoring active. Consider starting monitoring for better system insights.")

        return recommendations

    def cleanup_logs(self, days_to_keep: int = 30) -> int:
        """Clean up old log files."""
        print(f"🧹 Cleaning up logs older than {days_to_keep} days...")

        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cleaned_count = 0

        try:
            for log_file in self.logs_dir.rglob("*.log*"):
                if log_file.is_file():
                    file_mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_mtime < cutoff_date:
                        log_file.unlink()
                        cleaned_count += 1

            print(f"✅ Cleaned up {cleaned_count} old log files")
            return cleaned_count

        except Exception as e:
            print(f"❌ Error cleaning logs: {e}")
            return 0

    def interactive_mode(self) -> None:
        """Run interactive management mode."""
        print("🎮 ClaudeCode Interactive Management Mode")
        print("=" * 50)

        while True:
            print("\nAvailable commands:")
            print("  1. System Status")
            print("  2. Health Check")
            print("  3. Validate System")
            print("  4. Initialize Project")
            print("  5. Start Monitoring")
            print("  6. Stop Monitoring")
            print("  7. Generate Report")
            print("  8. Cleanup Logs")
            print("  9. Exit")

            try:
                choice = input("\nSelect option (1-9): ").strip()

                if choice == "1":
                    status = self.get_system_status()
                    print(json.dumps(status, indent=2, default=str))

                elif choice == "2":
                    self.health_check()

                elif choice == "3":
                    auto_fix = input("Auto-fix issues? (y/N): ").strip().lower() == 'y'
                    success, messages = self.validate_system(auto_fix)
                    for message in messages:
                        print(message)
                    print(f"Validation: {'✅ Success' if success else '❌ Failed'}")

                elif choice == "4":
                    project_name = input("Project name: ").strip()
                    if project_name:
                        project_type = input("Project type (web-app/api-service/data-science/library) [web-app]: ").strip() or "web-app"
                        github = input("Create GitHub repo? (y/N): ").strip().lower() == 'y'
                        self.initialize_project(project_name, project_type, create_github=github)

                elif choice == "5":
                    project_name = input("Project name [claude_code_system]: ").strip() or "claude_code_system"
                    self.start_monitoring(project_name)

                elif choice == "6":
                    project_name = input("Project name (blank for all): ").strip() or None
                    self.stop_monitoring(project_name)

                elif choice == "7":
                    filename = input("Output filename [system_report.json]: ").strip() or "system_report.json"
                    output_path = Path(filename)
                    self.generate_report(output_path)

                elif choice == "8":
                    days = input("Days to keep [30]: ").strip()
                    try:
                        days = int(days) if days else 30
                        self.cleanup_logs(days)
                    except ValueError:
                        print("Invalid number of days")

                elif choice == "9":
                    break

                else:
                    print("Invalid choice. Please select 1-9.")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

    def shutdown(self) -> None:
        """Graceful shutdown of all services."""
        print("🔄 Shutting down ClaudeCode Manager...")

        # Stop all monitoring
        self.stop_monitoring()

        # Close logger
        if self.logger:
            self.logger.close()

        print("✅ Shutdown complete")


def main():
    """Main entry point for ClaudeCode Manager."""
    parser = argparse.ArgumentParser(
        description="ClaudeCode AI Engineering Platform Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python claude_code_manager.py status
  python claude_code_manager.py validate --fix
  python claude_code_manager.py init-project --name "my-app" --type "web-app"
  python claude_code_manager.py start-monitoring --project "my-project"
  python claude_code_manager.py interactive
        """
    )

    parser.add_argument("--claude-code-root",
                       help="Path to ClaudeCode root directory")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    subparsers.add_parser("status", help="Show system status")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate system configuration")
    validate_parser.add_argument("--fix", action="store_true", help="Auto-fix issues")

    # Health check command
    subparsers.add_parser("health-check", help="Perform health check")

    # Initialize project command
    init_parser = subparsers.add_parser("init-project", help="Initialize new project")
    init_parser.add_argument("--name", required=True, help="Project name")
    init_parser.add_argument("--type", choices=["web-app", "api-service", "data-science", "library"],
                           default="web-app", help="Project type")
    init_parser.add_argument("--target-dir", help="Target directory")
    init_parser.add_argument("--github", action="store_true", help="Create GitHub repository")

    # Monitoring commands
    monitor_parser = subparsers.add_parser("start-monitoring", help="Start performance monitoring")
    monitor_parser.add_argument("--project", help="Project name")

    stop_monitor_parser = subparsers.add_parser("stop-monitoring", help="Stop performance monitoring")
    stop_monitor_parser.add_argument("--project", help="Project name")

    # Report command
    report_parser = subparsers.add_parser("generate-report", help="Generate system report")
    report_parser.add_argument("--output", help="Output file path")

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup-logs", help="Clean up old log files")
    cleanup_parser.add_argument("--days", type=int, default=30, help="Days to keep")

    # Interactive command
    subparsers.add_parser("interactive", help="Run in interactive mode")

    args = parser.parse_args()

    # Initialize manager
    manager = ClaudeCodeManager(args.claude_code_root)

    # Set up signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print("\nReceived shutdown signal...")
        manager.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Execute command
        if args.command == "status":
            status = manager.get_system_status()
            print(json.dumps(status, indent=2, default=str))

        elif args.command == "validate":
            success, messages = manager.validate_system(args.fix)
            for message in messages:
                print(message)
            sys.exit(0 if success else 1)

        elif args.command == "health-check":
            success = manager.health_check()
            sys.exit(0 if success else 1)

        elif args.command == "init-project":
            target_dir = Path(args.target_dir) if args.target_dir else None
            success = manager.initialize_project(
                args.name, args.type, target_dir, args.github
            )
            sys.exit(0 if success else 1)

        elif args.command == "start-monitoring":
            success = manager.start_monitoring(args.project)
            if success:
                print("Monitoring started. Press Ctrl+C to stop.")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    manager.stop_monitoring(args.project)
            sys.exit(0 if success else 1)

        elif args.command == "stop-monitoring":
            success = manager.stop_monitoring(args.project)
            sys.exit(0 if success else 1)

        elif args.command == "generate-report":
            output_path = Path(args.output) if args.output else None
            manager.generate_report(output_path)

        elif args.command == "cleanup-logs":
            manager.cleanup_logs(args.days)

        elif args.command == "interactive":
            manager.interactive_mode()

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        manager.shutdown()


if __name__ == "__main__":
    main()
