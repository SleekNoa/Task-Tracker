"""
Task Repository
"""

from typing import List
from app.domain.task import Task
from app.storage.json_storage import JSONStorage
from app.config import TASKS_FILE


class TaskRepository:
    """Repository for Task persistence."""
    
    def __init__(self, storage: JSONStorage = None):
        self.storage = storage or JSONStorage(TASKS_FILE)
    
    def get_all(self) -> List[Task]:
        records = self.storage.read()
        return [Task.from_dict(r) for r in records]
    
    def get_by_id(self, task_id: str) -> Task:
        record = self.storage.find_by("id", task_id)
        if record:
            return Task.from_dict(record)
        return None
    
    def save(self, task: Task) -> Task:
        record = task.to_dict()
        self.storage.append(record)
        return task
    
    def update(self, task: Task) -> bool:
        return self.storage.update("id", task.id, task.to_dict())
    
    def delete(self, task_id: str) -> bool:
        return self.storage.delete_by("id", task_id)