"""
Task domain model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Task:
    """Represents a task to be tracked."""
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "active"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", ""),
            created_at=data.get("created_at", datetime.now().isoformat()),
            status=data.get("status", "active")
        )