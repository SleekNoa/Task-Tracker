"""
Work Session domain model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class WorkSession:
    """Represents a completed work session."""
    task_id: str
    started_at: str
    ended_at: str
    duration_minutes: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "duration_minutes": self.duration_minutes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WorkSession':
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            task_id=data.get("task_id", ""),
            started_at=data.get("started_at", ""),
            ended_at=data.get("ended_at", ""),
            duration_minutes=data.get("duration_minutes", 60)
        )
    
    @classmethod
    def from_timer(cls, task_id: str, timer_data: dict) -> 'WorkSession':
        """Create a WorkSession from timer data."""
        started_at = timer_data.get("started_at", datetime.now().timestamp())
        started_str = datetime.fromtimestamp(started_at).isoformat()
        ended_str = datetime.now().isoformat()
        
        elapsed_seconds = datetime.now().timestamp() - started_at
        duration = max(1, round(elapsed_seconds / 60))
        
        return cls(
            task_id=task_id,
            started_at=started_str,
            ended_at=ended_str,
            duration_minutes=duration
        )