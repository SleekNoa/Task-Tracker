"""
Timer Service
"""

from typing import Optional
from app.domain.timer import Timer
from app.domain.work_session import WorkSession
from app.repositories.timer_repository import TimerRepository
from app.repositories.work_session_repository import WorkSessionRepository
from app.storage.json_storage import JSONStorage
from app.config import TASKS_FILE
from datetime import datetime


class TimerService:
    """Application service for timer management."""
    
    def __init__(self, timer_repository: TimerRepository = None, 
                 work_session_repository: WorkSessionRepository = None):
        self.timer_repository = timer_repository or TimerRepository()
        self.work_session_repository = work_session_repository or WorkSessionRepository()
    
    def start(self, task_title: str) -> Timer:
        """Start a timer for a task."""
        if not task_title or not task_title.strip():
            raise ValueError("Task title cannot be empty")
        
        timer = Timer(task_id=task_title.strip())
        return self.timer_repository.save(timer)
    
    def stop(self) -> Optional[WorkSession]:
        """Stop the active timer and create a work session."""
        timer = self.timer_repository.get_active()
        if not timer:
            return None
        
        # Create work session from timer
        session = WorkSession.from_timer(timer.task_id, timer.to_dict())
        
        # Save session
        self.work_session_repository.save(session)
        
        # Record to tasks.json for backward compatibility
        self._record_to_tasks_json(timer.task_id, session.duration_minutes)
        
        # Clear active timer
        self.timer_repository.clear_active()
        
        return session
    
    def get_active(self) -> Optional[Timer]:
        """Get the currently active timer."""
        return self.timer_repository.get_active()
    
    def is_active(self) -> bool:
        """Check if a timer is active."""
        return self.timer_repository.get_active() is not None
    
    def _record_to_tasks_json(self, task_title: str, duration_minutes: int):
        """Record timed task to tasks.json for backward compatibility."""
        storage = JSONStorage(TASKS_FILE)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "task": task_title,
            "duration_minutes": duration_minutes,
            "type": "timed"
        }
        storage.append(entry)