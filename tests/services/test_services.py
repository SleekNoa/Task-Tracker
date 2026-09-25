"""
Tests for services
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.task_service import TaskService
from app.services.timer_service import TimerService
from app.services.report_service import ReportService
from app.storage.json_storage import JSONStorage


def test_task_service():
    """Test TaskService operations."""
    # Create temp storage
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = JSONStorage(os.path.join(tmpdir, "test_tasks.json"))
        service = TaskService()
        service.task_repository.storage = storage
        
        # Create task
        task = service.create_task("Test Task")
        assert task.title == "Test Task"
        
        # Get all
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        
        print("PASS: TaskService tests")


def test_timer_service():
    """Test TimerService operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        timer_storage = JSONStorage(os.path.join(tmpdir, "timers.json"))
        session_storage = JSONStorage(os.path.join(tmpdir, "sessions.json"))
        tasks_storage = JSONStorage(os.path.join(tmpdir, "tasks.json"))
        
        service = TimerService()
        service.timer_repository.storage = timer_storage
        service.work_session_repository.storage = session_storage
        
        # Start timer
        timer = service.start("Test Task")
        assert timer.task_id == "Test Task"
        
        # Check active
        active = service.get_active()
        assert active is not None
        assert active.task_id == "Test Task"
        
        # Stop timer
        import time
        time.sleep(0.1)
        session = service.stop()
        assert session is not None
        assert session.duration_minutes >= 1
        
        print("PASS: TimerService tests")


def test_report_service():
    """Test ReportService operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_storage = JSONStorage(os.path.join(tmpdir, "tasks.json"))
        
        # Add test data
        tasks_storage.append({
            "timestamp": "2024-01-01T10:00:00",
            "date": "2024-01-01",
            "time": "10:00",
            "task": "Task A",
            "duration_minutes": 60
        })
        tasks_storage.append({
            "timestamp": "2024-01-01T11:00:00",
            "date": "2024-01-01",
            "time": "11:00",
            "task": "Task B",
            "duration_minutes": 30
        })
        
        service = ReportService()
        service.tasks_storage = tasks_storage
        
        summary = service.get_daily_summary("2024-01-01")
        assert summary["total_tasks"] == 2
        assert summary["total_time_minutes"] == 90
        
        print("PASS: ReportService tests")


if __name__ == "__main__":
    test_task_service()
    test_timer_service()
    test_report_service()
    print("\nAll service tests passed!")