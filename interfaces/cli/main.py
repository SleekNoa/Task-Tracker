"""
Task Tracker CLI Interface
Refactored to use application services.
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from app.services.task_service import TaskService
from app.services.timer_service import TimerService
from app.services.report_service import ReportService
from app.storage.json_storage import JSONStorage
from app.config import TASKS_FILE
from datetime import datetime


class TaskTrackerCLI:
    """Command-line interface for Task Tracker."""
    
    def __init__(self):
        self.task_service = TaskService()
        self.timer_service = TimerService()
        self.report_service = ReportService()
    
    def show_summary(self):
        """Display summary of tasks."""
        summary = self.report_service.get_daily_summary()
        
        if summary["total_tasks"] == 0:
            print(f"\nNo tasks found for {summary['date']}")
            return
        
        print(f"\n{'='*50}")
        print(f"TODAY'S SUMMARY - {summary['date']}")
        print(f"{'='*50}")
        print(f"Total Time: {summary['total_hours']}h ({summary['total_time_minutes']}m)")
        print(f"Unique Tasks: {summary['total_tasks']}")
        print(f"\n{'-'*50}")
        print(f"{'#':<3} {'Task':<35} {'Min':<6} {'Hours':<6}")
        print(f"{'-'*50}")
        
        for i, task in enumerate(summary['tasks'], 1):
            print(f"{i:<3} {task['task'][:33]:<35} {task['total_minutes']:<6} {task['hours']:<6.1f}")
    
    def add_task(self):
        """Add a task manually."""
        print("\nEnter task description (or press Enter to cancel):")
        task_text = input("> ").strip()
        
        if task_text:
            self.task_service.get_or_create_task(task_text)
            
            # Record to tasks.json for backward compatibility
            storage = JSONStorage(TASKS_FILE)
            entry = {
                "timestamp": datetime.now().isoformat(),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M"),
                "task": task_text,
                "duration_minutes": 60,
                "type": "hourly"
            }
            storage.append(entry)
            print(f"Added: {task_text}")
            return True
        return False
    
    def start_timer(self):
        """Start timed task tracking."""
        print("\nEnter task to track (or press Enter to cancel):")
        task_text = input("> ").strip()
        
        if task_text:
            self.timer_service.start(task_text)
            print(f"Timer started for: {task_text}")
            return True
        return False
    
    def stop_timer(self):
        """Stop timer and record session."""
        timer = self.timer_service.get_active()
        if timer:
            session = self.timer_service.stop()
            print(f"Timer stopped - Recorded {session.duration_minutes} minutes")
            return True
        else:
            print("No active timer")
            return False
    
    def run(self):
        """Main CLI loop."""
        print("="*50)
        print("TASK TRACKER - Console Version")
        print("="*50)
        
        while True:
            print(f"\n{'='*50}")
            print("Menu:")
            print("  1. Add task manually")
            print("  2. View today's summary")
            print("  3. Start timed task")
            print("  4. Stop timed task")
            print("  5. Exit")
            print(f"{'='*50}")
            
            choice = input("Select (1-5): ").strip()
            
            if choice == "1":
                self.add_task()
                self.show_summary()
            elif choice == "2":
                self.show_summary()
            elif choice == "3":
                self.start_timer()
            elif choice == "4":
                self.stop_timer()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice")


def main():
    cli = TaskTrackerCLI()
    cli.run()


if __name__ == "__main__":
    main()