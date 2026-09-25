"""
Work Session Repository
"""

from typing import List
from app.domain.work_session import WorkSession
from app.storage.json_storage import JSONStorage
from app.config import WORK_SESSIONS_FILE


class WorkSessionRepository:
    """Repository for WorkSession persistence."""
    
    def __init__(self, storage: JSONStorage = None):
        self.storage = storage or JSONStorage(WORK_SESSIONS_FILE)
    
    def get_all(self) -> List[WorkSession]:
        records = self.storage.read()
        return [WorkSession.from_dict(r) for r in records]
    
    def get_by_task(self, task_id: str) -> List[WorkSession]:
        records = self.storage.find_all_by("task_id", task_id)
        return [WorkSession.from_dict(r) for r in records]
    
    def save(self, session: WorkSession) -> WorkSession:
        self.storage.append(session.to_dict())
        return session
    
    def delete(self, session_id: str) -> bool:
        return self.storage.delete_by("id", session_id)