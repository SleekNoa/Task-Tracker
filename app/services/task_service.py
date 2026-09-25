"""
Task Service
"""

from typing import List, Optional
from datetime import datetime
from app.domain.task import Task
from app.repositories.task_repository import TaskRepository


class TaskService:
    """Application service for task management."""
    
    def __init__(self, task_repository: TaskRepository = None):
        self.task_repository = task_repository or TaskRepository()
    
    def create_task(self, title: str) -> Task:
        """Create a new task."""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        
        task = Task(title=title.strip())
        return self.task_repository.save(task)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.task_repository.get_all()
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.task_repository.get_by_id(task_id)
    
    def get_tasks_for_date(self, date: str) -> List[dict]:
        """Get tasks for a specific date (for backward compatibility with existing data)."""
        # For backward compatibility with existing tasks.json format
        from app.storage.json_storage import JSONStorage
        from app.config import TASKS_FILE
        
        storage = JSONStorage(TASKS_FILE)
        records = storage.read()
        return [r for r in records if r.get("date") == date]
    
    def get_or_create_task(self, title: str) -> Task:
        """Get existing task or create new one."""
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.title == title:
                return task
        return self.create_task(title)
    
    def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed."""
        task = self.get_task_by_id(task_id)
        if task:
            task.status = "completed"
            return self.task_repository.update(task)
        return False
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        return self.task_repository.delete(task_id)