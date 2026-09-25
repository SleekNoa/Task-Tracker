"""
Tests for domain models
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.domain.task import Task
from app.domain.timer import Timer
from app.domain.work_session import WorkSession


def test_task_creation():
    """Test Task model creation."""
    task = Task(title="Test Task")
    assert task.title == "Test Task"
    assert task.id is not None
    assert task.status == "active"
    print("PASS: Task creation")


def test_task_to_dict():
    """Test Task serialization."""
    task = Task(title="Test Task")
    data = task.to_dict()
    assert data["title"] == "Test Task"
    assert "id" in data
    print("PASS: Task to_dict")


def test_task_from_dict():
    """Test Task deserialization."""
    data = {"id": "123", "title": "Test", "created_at": "2024-01-01", "status": "active"}
    task = Task.from_dict(data)
    assert task.id == "123"
    assert task.title == "Test"
    print("PASS: Task from_dict")


def test_timer_creation():
    """Test Timer model creation."""
    timer = Timer(task_id="task-123")
    assert timer.task_id == "task-123"
    assert timer.active == True
    print("PASS: Timer creation")


def test_timer_elapsed():
    """Test Timer elapsed time calculation."""
    import time
    timer = Timer(task_id="task-123")
    time.sleep(0.1)
    elapsed = timer.get_elapsed_seconds()
    assert elapsed >= 0.1
    print("PASS: Timer elapsed")


def test_work_session_creation():
    """Test WorkSession model creation."""
    session = WorkSession(
        task_id="task-123",
        started_at="2024-01-01T10:00:00",
        ended_at="2024-01-01T11:00:00",
        duration_minutes=60
    )
    assert session.task_id == "task-123"
    assert session.duration_minutes == 60
    print("PASS: WorkSession creation")


if __name__ == "__main__":
    test_task_creation()
    test_task_to_dict()
    test_task_from_dict()
    test_timer_creation()
    test_timer_elapsed()
    test_work_session_creation()
    print("\nAll domain tests passed!")