"""
Timer Repository
"""

from typing import Optional
from app.domain.timer import Timer
from app.storage.json_storage import JSONStorage
from app.config import TIMERS_FILE


class TimerRepository:
    """Repository for Timer persistence."""
    
    def __init__(self, storage: JSONStorage = None):
        self.storage = storage or JSONStorage(TIMERS_FILE)
    
    def get_active(self) -> Optional[Timer]:
        records = self.storage.read()
        for record in records:
            if record.get("active", False):
                return Timer.from_dict(record)
        return None
    
    def save(self, timer: Timer) -> Timer:
        # Clear any existing active timers first
        self.clear_active()
        self.storage.append(timer.to_dict())
        return timer
    
    def clear_active(self):
        """Clear all active timers."""
        records = self.storage.read()
        records = [r for r in records if not r.get("active", False)]
        self.storage.write(records)
    
    def clear_all(self):
        """Clear all timer records."""
        self.storage.clear()