"""
Task Tracker Console App
Works without tkinter - runs in command prompt.
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import time
import threading

# Configuration
INTERVAL_MINUTES = 60
DATA_FILE = "tasks.json"

def load_tasks():
    """Load existing tasks from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def show_summary(tasks):
    """Display summary of tasks"""
    today = datetime.now().strftime("%Y-%m-%d")
    daily_tasks = [t for t in tasks if t.get("date") == today]
    
    if not daily_tasks:
        print(f"\nNo tasks found for {today}")
        return
    
    # Aggregate
    task_totals = defaultdict(lambda: {"count": 0, "total_minutes": 0})
    for task in daily_tasks:
        task_totals[task["task"]]["count"] += 1
        task_totals[task["task"]]["total_minutes"] += task.get("duration_minutes", 60)
    
    total_minutes = sum(v["total_minutes"] for v in task_totals.values())
    total_hours = round(total_minutes / 60, 1)
    
    print(f"\n{'='*50}")
    print(f"TODAY'S SUMMARY - {today}")
    print(f"{'='*50}")
    print(f"Total Time: {total_hours}h ({total_minutes}m)")
    print(f"Unique Tasks: {len(task_totals)}")
    print(f"\n{'-'*50}")
    print(f"{'#':<3} {'Task':<35} {'Min':<6} {'Hours':<6}")
    print(f"{'-'*50}")
    
    for i, (task, data) in enumerate(sorted(task_totals.items(), key=lambda x: x[1]["total_minutes"], reverse=True), 1):
        print(f"{i:<3} {task[:33]:<35} {data['total_minutes']:<6} {data['total_minutes']/60:<6.1f}")

def add_task(tasks):
    """Add a task manually"""
    print("\nEnter task description (or press Enter to cancel):")
    task_text = input("> ").strip()
    
    if task_text:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "task": task_text,
            "duration_minutes": INTERVAL_MINUTES
        }
        tasks.append(entry)
        save_tasks(tasks)
        print(f"Added: {task_text}")
        return True
    return False

def run_scheduler(tasks, running_flag):
    """Run the popup scheduler in background"""
    while running_flag[0]:
        time.sleep(INTERVAL_MINUTES * 60)
        if running_flag[0]:
            print(f"\n[{datetime.now().strftime('%H:%M')}] Time to log your task!")
            add_task(tasks)

def main():
    print("="*50)
    print("TASK TRACKER - Console Version")
    print("="*50)
    
    tasks = load_tasks()
    running_flag = [False]  # Use list for mutability in thread
    
    while True:
        print(f"\n{'='*50}")
        print("Menu:")
        print("  1. Add task manually")
        print("  2. View today's summary")
        print("  3. Start timer (prompts every 60 min)")
        print("  4. Stop timer")
        print("  5. Exit")
        print(f"{'='*50}")
        
        choice = input("Select (1-5): ").strip()
        
        if choice == "1":
            add_task(tasks)
            tasks = load_tasks()  # Reload
            show_summary(tasks)
        elif choice == "2":
            show_summary(tasks)
        elif choice == "3":
            if not running_flag[0]:
                running_flag[0] = True
                print("Timer started - will prompt every 60 minutes")
                threading.Thread(target=run_scheduler, args=(tasks, running_flag), daemon=True).start()
            else:
                print("Timer already running")
        elif choice == "4":
            running_flag[0] = False
            print("Timer stopped")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()