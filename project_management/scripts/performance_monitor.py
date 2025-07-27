#!/usr/bin/env python3
"""
ClaudeCode Performance Monitoring & Analytics System
===================================================

Advanced performance monitoring system that tracks system health, response times,
resource usage, and provides analytics for AI development sessions and workflows.

Usage:
    from performance_monitor import PerformanceMonitor, SystemHealthTracker

    monitor = PerformanceMonitor("my_project")
    health = SystemHealthTracker(monitor)

    monitor.start_monitoring()
    # ... development work ...
    monitor.stop_monitoring()

Features:
    - Real-time system resource monitoring
    - AI response time tracking
    - Workflow performance analysis
    - Memory and CPU usage monitoring
    - Custom metric collection
    - Performance alerts and thresholds
    - Historical trend analysis
    - Automated performance reports
    - Resource optimization suggestions
"""

import json
import os
import psutil
import threading
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import subprocess
import platform


class MetricType(Enum):
    """Types of performance metrics."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class PerformanceMetric:
    """A single performance metric measurement."""
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    labels: Dict[str, str]
    unit: str = "count"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "value": self.value,
            "metric_type": self.metric_type.value,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels,
            "unit": self.unit
        }


@dataclass
class PerformanceAlert:
    """Performance alert when thresholds are exceeded."""
    alert_id: str
    metric_name: str
    current_value: float
    threshold_value: float
    level: AlertLevel
    message: str
    timestamp: datetime
    resolved: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "alert_id": self.alert_id,
            "metric_name": self.metric_name,
            "current_value": self.current_value,
            "threshold_value": self.threshold_value,
            "level": self.level.value,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved
        }


class MetricCollector:
    """Collects and stores performance metrics."""

    def __init__(self, max_history: int = 10000):
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self.counters: Dict[str, float] = defaultdict(float)
        self.gauges: Dict[str, float] = defaultdict(float)
        self._lock = threading.Lock()

    def record_metric(self, name: str, value: float, metric_type: MetricType,
                     labels: Optional[Dict[str, str]] = None, unit: str = "count") -> None:
        """Record a performance metric."""
        with self._lock:
            metric = PerformanceMetric(
                name=name,
                value=value,
                metric_type=metric_type,
                timestamp=datetime.now(),
                labels=labels or {},
                unit=unit
            )

            self.metrics[name].append(metric)

            # Update aggregated values
            if metric_type == MetricType.COUNTER:
                self.counters[name] += value
            elif metric_type == MetricType.GAUGE:
                self.gauges[name] = value

    def increment_counter(self, name: str, value: float = 1.0,
                         labels: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter metric."""
        self.record_metric(name, value, MetricType.COUNTER, labels)

    def set_gauge(self, name: str, value: float,
                  labels: Optional[Dict[str, str]] = None, unit: str = "count") -> None:
        """Set a gauge metric value."""
        self.record_metric(name, value, MetricType.GAUGE, labels, unit)

    def record_timing(self, name: str, duration_ms: float,
                     labels: Optional[Dict[str, str]] = None) -> None:
        """Record a timing measurement."""
        self.record_metric(name, duration_ms, MetricType.TIMER, labels, "milliseconds")

    def get_metric_history(self, name: str,
                          time_window_minutes: Optional[int] = None) -> List[PerformanceMetric]:
        """Get metric history, optionally filtered by time window."""
        with self._lock:
            if name not in self.metrics:
                return []

            metrics = list(self.metrics[name])

            if time_window_minutes:
                cutoff = datetime.now() - timedelta(minutes=time_window_minutes)
                metrics = [m for m in metrics if m.timestamp > cutoff]

            return metrics

    def get_metric_stats(self, name: str,
                        time_window_minutes: Optional[int] = None) -> Dict[str, Any]:
        """Get statistical summary of a metric."""
        history = self.get_metric_history(name, time_window_minutes)

        if not history:
            return {}

        values = [m.value for m in history]

        return {
            "name": name,
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "latest": values[-1],
            "first": values[0],
            "time_range_minutes": time_window_minutes
        }


class SystemResourceMonitor:
    """Monitors system resources like CPU, memory, disk, network."""

    def __init__(self, collector: MetricCollector):
        self.collector = collector
        self.monitoring = False
        self.monitor_thread = None
        self.monitor_interval = 5.0  # seconds

    def start_monitoring(self) -> None:
        """Start continuous system monitoring."""
        if self.monitoring:
            return

        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self) -> None:
        """Stop system monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)

    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring:
            try:
                self._collect_cpu_metrics()
                self._collect_memory_metrics()
                self._collect_disk_metrics()
                self._collect_network_metrics()
                self._collect_process_metrics()

                time.sleep(self.monitor_interval)
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(self.monitor_interval)

    def _collect_cpu_metrics(self) -> None:
        """Collect CPU usage metrics."""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else (0, 0, 0)

        self.collector.set_gauge("system_cpu_percent", cpu_percent, unit="percent")
        self.collector.set_gauge("system_cpu_count", cpu_count, unit="count")
        self.collector.set_gauge("system_load_1min", load_avg[0], unit="load")
        self.collector.set_gauge("system_load_5min", load_avg[1], unit="load")
        self.collector.set_gauge("system_load_15min", load_avg[2], unit="load")

    def _collect_memory_metrics(self) -> None:
        """Collect memory usage metrics."""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        self.collector.set_gauge("system_memory_total", memory.total / (1024**3), unit="GB")
        self.collector.set_gauge("system_memory_used", memory.used / (1024**3), unit="GB")
        self.collector.set_gauge("system_memory_percent", memory.percent, unit="percent")
        self.collector.set_gauge("system_memory_available", memory.available / (1024**3), unit="GB")

        self.collector.set_gauge("system_swap_total", swap.total / (1024**3), unit="GB")
        self.collector.set_gauge("system_swap_used", swap.used / (1024**3), unit="GB")
        self.collector.set_gauge("system_swap_percent", swap.percent, unit="percent")

    def _collect_disk_metrics(self) -> None:
        """Collect disk usage metrics."""
        disk_usage = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()

        self.collector.set_gauge("system_disk_total", disk_usage.total / (1024**3), unit="GB")
        self.collector.set_gauge("system_disk_used", disk_usage.used / (1024**3), unit="GB")
        self.collector.set_gauge("system_disk_percent", (disk_usage.used / disk_usage.total) * 100, unit="percent")

        if disk_io:
            self.collector.set_gauge("system_disk_read_bytes", disk_io.read_bytes, unit="bytes")
            self.collector.set_gauge("system_disk_write_bytes", disk_io.write_bytes, unit="bytes")

    def _collect_network_metrics(self) -> None:
        """Collect network usage metrics."""
        try:
            net_io = psutil.net_io_counters()
            if net_io:
                self.collector.set_gauge("system_network_bytes_sent", net_io.bytes_sent, unit="bytes")
                self.collector.set_gauge("system_network_bytes_recv", net_io.bytes_recv, unit="bytes")
                self.collector.set_gauge("system_network_packets_sent", net_io.packets_sent, unit="count")
                self.collector.set_gauge("system_network_packets_recv", net_io.packets_recv, unit="count")
        except Exception:
            pass  # Network metrics may not be available on all systems

    def _collect_process_metrics(self) -> None:
        """Collect current process metrics."""
        try:
            process = psutil.Process()

            cpu_percent = process.cpu_percent()
            memory_info = process.memory_info()
            num_threads = process.num_threads()

            self.collector.set_gauge("process_cpu_percent", cpu_percent, unit="percent")
            self.collector.set_gauge("process_memory_rss", memory_info.rss / (1024**2), unit="MB")
            self.collector.set_gauge("process_memory_vms", memory_info.vms / (1024**2), unit="MB")
            self.collector.set_gauge("process_threads", num_threads, unit="count")
        except Exception:
            pass  # Process metrics may not be available


class AlertManager:
    """Manages performance alerts and thresholds."""

    def __init__(self, collector: MetricCollector):
        self.collector = collector
        self.thresholds: Dict[str, Dict[str, Any]] = {}
        self.active_alerts: Dict[str, PerformanceAlert] = {}
        self.alert_history: List[PerformanceAlert] = []
        self.alert_callbacks: List[Callable[[PerformanceAlert], None]] = []

    def set_threshold(self, metric_name: str, threshold_value: float,
                     comparison: str = "greater", level: AlertLevel = AlertLevel.WARNING,
                     message_template: Optional[str] = None) -> None:
        """Set an alert threshold for a metric."""
        self.thresholds[metric_name] = {
            "threshold_value": threshold_value,
            "comparison": comparison,  # "greater", "less", "equal"
            "level": level,
            "message_template": message_template or f"{metric_name} threshold exceeded"
        }

    def add_alert_callback(self, callback: Callable[[PerformanceAlert], None]) -> None:
        """Add a callback function to be called when alerts are triggered."""
        self.alert_callbacks.append(callback)

    def check_thresholds(self) -> List[PerformanceAlert]:
        """Check all metrics against their thresholds."""
        new_alerts = []

        for metric_name, threshold_config in self.thresholds.items():
            latest_metrics = self.collector.get_metric_history(metric_name, time_window_minutes=1)

            if not latest_metrics:
                continue

            latest_value = latest_metrics[-1].value
            threshold_value = threshold_config["threshold_value"]
            comparison = threshold_config["comparison"]

            # Check if threshold is exceeded
            threshold_exceeded = False
            if comparison == "greater" and latest_value > threshold_value:
                threshold_exceeded = True
            elif comparison == "less" and latest_value < threshold_value:
                threshold_exceeded = True
            elif comparison == "equal" and abs(latest_value - threshold_value) < 0.001:
                threshold_exceeded = True

            alert_key = f"{metric_name}_{comparison}_{threshold_value}"

            if threshold_exceeded:
                if alert_key not in self.active_alerts:
                    # Create new alert
                    alert = PerformanceAlert(
                        alert_id=str(uuid.uuid4()),
                        metric_name=metric_name,
                        current_value=latest_value,
                        threshold_value=threshold_value,
                        level=threshold_config["level"],
                        message=threshold_config["message_template"].format(
                            metric_name=metric_name,
                            current_value=latest_value,
                            threshold_value=threshold_value
                        ),
                        timestamp=datetime.now()
                    )

                    self.active_alerts[alert_key] = alert
                    self.alert_history.append(alert)
                    new_alerts.append(alert)

                    # Trigger callbacks
                    for callback in self.alert_callbacks:
                        try:
                            callback(alert)
                        except Exception as e:
                            print(f"Error in alert callback: {e}")
            else:
                # Resolve alert if it exists
                if alert_key in self.active_alerts:
                    alert = self.active_alerts[alert_key]
                    alert.resolved = True
                    del self.active_alerts[alert_key]

        return new_alerts


class PerformanceAnalyzer:
    """Analyzes performance data and provides insights."""

    def __init__(self, collector: MetricCollector):
        self.collector = collector

    def analyze_trends(self, metric_name: str,
                      time_window_hours: int = 24) -> Dict[str, Any]:
        """Analyze trends for a specific metric."""
        history = self.collector.get_metric_history(metric_name, time_window_hours * 60)

        if len(history) < 2:
            return {"error": "Insufficient data for trend analysis"}

        values = [m.value for m in history]
        timestamps = [m.timestamp for m in history]

        # Simple linear trend calculation
        n = len(values)
        sum_x = sum(range(n))
        sum_y = sum(values)
        sum_xy = sum(i * values[i] for i in range(n))
        sum_x2 = sum(i * i for i in range(n))

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n

        # Determine trend direction
        if slope > 0.01:
            trend = "increasing"
        elif slope < -0.01:
            trend = "decreasing"
        else:
            trend = "stable"

        return {
            "metric_name": metric_name,
            "trend": trend,
            "slope": slope,
            "intercept": intercept,
            "data_points": n,
            "time_window_hours": time_window_hours,
            "latest_value": values[-1],
            "first_value": values[0],
            "percent_change": ((values[-1] - values[0]) / values[0]) * 100 if values[0] != 0 else 0
        }

    def identify_anomalies(self, metric_name: str,
                          sensitivity: float = 2.0) -> List[Dict[str, Any]]:
        """Identify anomalies in metric data using statistical methods."""
        history = self.collector.get_metric_history(metric_name, 60)  # Last hour

        if len(history) < 10:
            return []

        values = [m.value for m in history]
        mean_val = statistics.mean(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0

        anomalies = []
        for i, metric in enumerate(history):
            z_score = abs(metric.value - mean_val) / std_dev if std_dev > 0 else 0

            if z_score > sensitivity:
                anomalies.append({
                    "timestamp": metric.timestamp.isoformat(),
                    "value": metric.value,
                    "z_score": z_score,
                    "deviation_from_mean": metric.value - mean_val
                })

        return anomalies

    def generate_performance_report(self,
                                   time_window_hours: int = 24) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "time_window_hours": time_window_hours,
            "system_health": {},
            "performance_trends": {},
            "anomalies": {},
            "recommendations": []
        }

        # Key system metrics to analyze
        key_metrics = [
            "system_cpu_percent",
            "system_memory_percent",
            "system_disk_percent",
            "process_cpu_percent",
            "process_memory_rss"
        ]

        for metric in key_metrics:
            # Get basic stats
            stats = self.collector.get_metric_stats(metric, time_window_hours * 60)
            if stats:
                report["system_health"][metric] = stats

                # Analyze trends
                trends = self.analyze_trends(metric, time_window_hours)
                report["performance_trends"][metric] = trends

                # Find anomalies
                anomalies = self.identify_anomalies(metric)
                if anomalies:
                    report["anomalies"][metric] = anomalies

        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(report)

        return report

    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate performance optimization recommendations."""
        recommendations = []

        # Check CPU usage
        cpu_stats = report["system_health"].get("system_cpu_percent", {})
        if cpu_stats.get("mean", 0) > 80:
            recommendations.append("High average CPU usage detected. Consider optimizing CPU-intensive operations.")

        # Check memory usage
        memory_stats = report["system_health"].get("system_memory_percent", {})
        if memory_stats.get("mean", 0) > 85:
            recommendations.append("High memory usage detected. Consider implementing memory optimization strategies.")

        # Check disk usage
        disk_stats = report["system_health"].get("system_disk_percent", {})
        if disk_stats.get("latest", 0) > 90:
            recommendations.append("Disk space is running low. Consider cleaning up old files or expanding storage.")

        # Check for increasing trends
        for metric, trend_data in report["performance_trends"].items():
            if trend_data.get("trend") == "increasing":
                if "cpu" in metric and trend_data.get("percent_change", 0) > 20:
                    recommendations.append(f"CPU usage is trending upward. Monitor for performance degradation.")
                elif "memory" in metric and trend_data.get("percent_change", 0) > 20:
                    recommendations.append(f"Memory usage is trending upward. Check for memory leaks.")

        # Check for anomalies
        total_anomalies = sum(len(anomalies) for anomalies in report["anomalies"].values())
        if total_anomalies > 5:
            recommendations.append("Multiple performance anomalies detected. Review system logs for issues.")

        return recommendations


class PerformanceMonitor:
    """Main performance monitoring system coordinator."""

    def __init__(self, project_name: str, log_dir: Optional[Path] = None):
        self.project_name = project_name
        self.log_dir = log_dir or Path.cwd() / "logs" / "performance"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.collector = MetricCollector()
        self.system_monitor = SystemResourceMonitor(self.collector)
        self.alert_manager = AlertManager(self.collector)
        self.analyzer = PerformanceAnalyzer(self.collector)

        # Configuration
        self.monitoring_active = False
        self.report_interval_minutes = 60
        self.report_thread = None

        # Set default thresholds
        self._set_default_thresholds()

        # Add default alert callback
        self.alert_manager.add_alert_callback(self._handle_alert)

    def _set_default_thresholds(self) -> None:
        """Set default performance thresholds."""
        self.alert_manager.set_threshold("system_cpu_percent", 90.0, "greater", AlertLevel.WARNING)
        self.alert_manager.set_threshold("system_memory_percent", 90.0, "greater", AlertLevel.WARNING)
        self.alert_manager.set_threshold("system_disk_percent", 95.0, "greater", AlertLevel.CRITICAL)
        self.alert_manager.set_threshold("process_memory_rss", 1024.0, "greater", AlertLevel.WARNING)

    def _handle_alert(self, alert: PerformanceAlert) -> None:
        """Default alert handler."""
        print(f"🚨 ALERT [{alert.level.value.upper()}]: {alert.message}")

        # Log to file
        alert_log_file = self.log_dir / "alerts.jsonl"
        with open(alert_log_file, "a") as f:
            f.write(json.dumps(alert.to_dict()) + "\n")

    def start_monitoring(self) -> None:
        """Start comprehensive performance monitoring."""
        if self.monitoring_active:
            return

        print(f"🔍 Starting performance monitoring for {self.project_name}")

        self.monitoring_active = True

        # Start system monitoring
        self.system_monitor.start_monitoring()

        # Start periodic reporting
        self.report_thread = threading.Thread(target=self._report_loop, daemon=True)
        self.report_thread.start()

        # Start alert checking
        self._start_alert_checking()

    def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        if not self.monitoring_active:
            return

        print(f"⏹️ Stopping performance monitoring for {self.project_name}")

        self.monitoring_active = False

        # Stop system monitoring
        self.system_monitor.stop_monitoring()

        # Wait for report thread
        if self.report_thread:
            self.report_thread.join(timeout=5.0)

    def _start_alert_checking(self) -> None:
        """Start periodic alert checking."""
        def alert_check_loop():
            while self.monitoring_active:
                try:
                    self.alert_manager.check_thresholds()
                    time.sleep(30)  # Check every 30 seconds
                except Exception as e:
                    print(f"Error in alert checking: {e}")
                    time.sleep(30)

        alert_thread = threading.Thread(target=alert_check_loop, daemon=True)
        alert_thread.start()

    def _report_loop(self) -> None:
        """Periodic performance reporting loop."""
        while self.monitoring_active:
            try:
                # Generate and save performance report
                report = self.analyzer.generate_performance_report(1)  # Last hour

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_file = self.log_dir / f"performance_report_{timestamp}.json"

                with open(report_file, "w") as f:
                    json.dump(report, f, indent=2, default=str)

                time.sleep(self.report_interval_minutes * 60)
            except Exception as e:
                print(f"Error in reporting loop: {e}")
                time.sleep(self.report_interval_minutes * 60)

    def time_operation(self, operation_name: str):
        """Context manager for timing operations."""
        return TimingContext(self.collector, operation_name)

    def record_ai_interaction(self, interaction_type: str, duration_ms: float,
                            success: bool = True, tokens_used: Optional[int] = None) -> None:
        """Record AI interaction performance metrics."""
        labels = {
            "interaction_type": interaction_type,
            "success": str(success)
        }

        self.collector.record_timing(f"ai_interaction_{interaction_type}", duration_ms, labels)
        self.collector.increment_counter("ai_interactions_total", labels=labels)

        if not success:
            self.collector.increment_counter("ai_interactions_failed", labels=labels)

        if tokens_used:
            self.collector.set_gauge("ai_tokens_used", tokens_used, labels=labels, unit="tokens")

    def record_workflow_performance(self, workflow_name: str, stage: str,
                                   duration_ms: float, success: bool = True) -> None:
        """Record workflow performance metrics."""
        labels = {
            "workflow": workflow_name,
            "stage": stage,
            "success": str(success)
        }

        self.collector.record_timing(f"workflow_{workflow_name}_{stage}", duration_ms, labels)
        self.collector.increment_counter("workflow_stages_total", labels=labels)

        if not success:
            self.collector.increment_counter("workflow_stages_failed", labels=labels)

    def get_current_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        key_metrics = [
            "system_cpu_percent",
            "system_memory_percent",
            "system_disk_percent",
            "process_memory_rss"
        ]

        stats = {}
        for metric in key_metrics:
            metric_stats = self.collector.get_metric_stats(metric, 5)  # Last 5 minutes
            if metric_stats:
                stats[metric] = metric_stats

        return {
            "timestamp": datetime.now().isoformat(),
            "project": self.project_name,
            "monitoring_active": self.monitoring_active,
            "active_alerts": len(self.alert_manager.active_alerts),
            "metrics": stats
        }


class TimingContext:
    """Context manager for timing operations."""

    def __init__(self, collector: MetricCollector, operation_name: str):
        self.collector = collector
        self.operation_name = operation_name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration_ms = (time.time() - self.start_time) * 1000
            success = exc_type is None

            labels = {"success": str(success)}
            self.collector.record_timing(self.operation_name, duration_ms, labels)


# Convenience functions
def create_performance_monitor(project_name: str) -> PerformanceMonitor:
    """Create a configured performance monitor for a project."""
    return PerformanceMonitor(project_name)


# Example usage
if __name__ == "__main__":
    # Example usage of the performance monitoring system
    monitor = create_performance_monitor("test_project")

    # Start monitoring
    monitor.start_monitoring()

    # Simulate some operations
    time.sleep(2)

    # Time an operation
    with monitor.time_operation("example_operation"):
        time.sleep(0.1)  # Simulate work

    # Record AI interaction
    monitor.record_ai_interaction("code_generation", 1500, success=True, tokens_used=250)

    # Record workflow performance
    monitor.record_workflow_performance("tdd_workflow", "test_writing", 800, success=True)

    # Get current stats
    stats = monitor.get_current_stats()
    print("Current stats:", json.dumps(stats, indent=2, default=str))

    # Let it run for a bit
    time.sleep(5)

    # Stop monitoring
    monitor.stop_monitoring()

    print("Performance monitoring example completed")
