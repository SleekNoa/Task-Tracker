"""
Timer domain model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Timer:
    """Represents an active timer for tracking work time."""
    task_id: str
    started_at: float = field(default_factory=lambda: datetime.now().timestamp())
    active: bool = True
    
    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "started_at": self.started_at,
            "active": self.active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Timer':
        return cls(
            task_id=data.get("task_id") or data.get("task", ""),
            started_at=data.get("started_at", datetime.now().timestamp()),
            active=data.get("active", True)
        )
    
    def get_elapsed_seconds(self) -> float:
        """Calculate elapsed time since timer started."""
        return datetime.now().timestamp() - self.started_at
    
    def get_elapsed_minutes(self) -> int:
        """Calculate elapsed time in minutes (minimum 1)."""
        return max(1, round(self.get_elapsed_seconds() / 60))