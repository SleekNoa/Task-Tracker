"""
Daily Summary Report Generator
Reads task data from JSON and generates summary reports.
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict
import os

DATA_FILE = "tasks.json"
REPORT_FILE = "daily_summary.json"


def load_tasks():
    """Load tasks from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []


def generate_daily_summary(target_date=None):
    """
    Generate a summary of tasks for a specific date.
    
    Args:
        target_date: Date string in YYYY-MM-DD format. Defaults to today.
    
    Returns:
        Dictionary with daily summary data
    """
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    
    tasks = load_tasks()
    daily_tasks = [t for t in tasks if t.get("date") == target_date]
    
    if not daily_tasks:
        return {
            "date": target_date,
            "total_tasks": 0,
            "total_time_minutes": 0,
            "tasks": [],
            "summary": "No tasks recorded for this date."
        }
    
    # Group tasks by description and sum durations
    task_totals = defaultdict(lambda: {"count": 0, "total_minutes": 0, "entries": []})
    
    for task in daily_tasks:
        task_desc = task.get("task", "Unknown")
        duration = task.get("duration_minutes", 60)
        task_totals[task_desc]["count"] += 1
        task_totals[task_desc]["total_minutes"] += duration
        task_totals[task_desc]["entries"].append(task)
    
    # Build summary
    total_time = sum(item["total_minutes"] for item in task_totals.values())
    
    tasks_list = []
    for task_desc, data in task_totals.items():
        tasks_list.append({
            "task": task_desc,
            "total_minutes": data["total_minutes"],
            "entry_count": data["count"],
            "hours": round(data["total_minutes"] / 60, 2)
        })
    
    # Sort by time spent (descending)
    tasks_list.sort(key=lambda x: x["total_minutes"], reverse=True)
    
    summary = {
        "date": target_date,
        "total_tasks": len(tasks_list),
        "total_time_minutes": total_time,
        "total_hours": round(total_time / 60, 2),
        "tasks": tasks_list,
        "generated_at": datetime.now().isoformat()
    }
    
    return summary


def save_summary(summary):
    """Save summary to JSON file"""
    # Load existing summaries or create new list
    summaries = []
    if os.path.exists(REPORT_FILE):
        try:
            with open(REPORT_FILE, 'r') as f:
                summaries = json.load(f)
                if not isinstance(summaries, list):
                    summaries = []
        except (json.JSONDecodeError, FileNotFoundError):
            summaries = []
    
    # Remove existing summary for same date if present
    summaries = [s for s in summaries if s.get("date") != summary["date"]]
    
    # Add new summary
    summaries.append(summary)
    
    # Sort by date descending
    summaries.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    with open(REPORT_FILE, 'w') as f:
        json.dump(summaries, f, indent=2)


def print_summary_report(target_date=None):
    """Print a formatted summary to console"""
    summary = generate_daily_summary(target_date)
    
    print("\n" + "="*50)
    print(f"DAILY TASK SUMMARY - {summary['date']}")
    print("="*50)
    
    if summary["total_tasks"] == 0:
        print(summary["summary"])
        return
    
    print(f"\nTotal Time: {summary['total_hours']} hours ({summary['total_time_minutes']} minutes)")
    print(f"Unique Tasks: {summary['total_tasks']}\n")
    
    print("-"*50)
    print(f"{'Task':<30} {'Minutes':<10} {'Hours':<8}")
    print("-"*50)
    
    for task in summary["tasks"]:
        print(f"{task['task'][:28]:<30} {task['total_minutes']:<10} {task['hours']:<8.2f}")
    
    print("-"*50 + "\n")


def main():
    """Generate and save today's summary"""
    summary = generate_daily_summary()
    save_summary(summary)
    print_summary_report()
    print(f"Summary saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()