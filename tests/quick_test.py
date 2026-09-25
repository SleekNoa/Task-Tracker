"""
Quick Test - Creates sample data and generates all reports
Run this to verify everything works without user interaction.
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import sys

# Add parent directory to path for imports
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PARENT_DIR)

from visualization import create_task_distribution_chart, create_daily_timeline_chart, create_weekly_summary_chart

# Paths - write to parent directory
DATA_FILE = os.path.join(PARENT_DIR, "tasks.json")
SUMMARY_FILE = os.path.join(PARENT_DIR, "daily_summary.json")
PIE_FILE = os.path.join(PARENT_DIR, "task_distribution.png")
TIMELINE_FILE = os.path.join(PARENT_DIR, "daily_timeline.png")
WEEKLY_FILE = os.path.join(PARENT_DIR, "weekly_summary.png")

print("="*50)
print("TASK TRACKER - QUICK TEST")
print("="*50)

# Step 1: Create sample data
print("\n[1/3] Creating sample data...")
today = datetime.now().strftime("%Y-%m-%d")
tasks = [
    {"timestamp": datetime.now().isoformat(), "date": today, "time": "09:00:00", "task": "Morning standup and emails", "duration_minutes": 60},
    {"timestamp": datetime.now().isoformat(), "date": today, "time": "10:00:00", "task": "Feature development - Task Tracker", "duration_minutes": 120},
    {"timestamp": datetime.now().isoformat(), "date": today, "time": "12:00:00", "task": "Lunch break", "duration_minutes": 60},
    {"timestamp": datetime.now().isoformat(), "date": today, "time": "13:00:00", "task": "Feature development - Task Tracker", "duration_minutes": 60},
    {"timestamp": datetime.now().isoformat(), "date": today, "time": "14:00:00", "task": "Code review", "duration_minutes": 60}
]

with open(DATA_FILE, 'w') as f:
    json.dump(tasks, f, indent=2)
print(f"[OK] Created {len(tasks)} sample tasks")

# Step 2: Generate summary
print("\n[2/3] Generating summary report...")
task_totals = defaultdict(lambda: {"count": 0, "total_minutes": 0})
for task in tasks:
    task_totals[task["task"]]["count"] += 1
    task_totals[task["task"]]["total_minutes"] += task["duration_minutes"]

total_time = sum(item["total_minutes"] for item in task_totals.values())

summary = {
    "date": today,
    "total_tasks": len(task_totals),
    "total_time_minutes": total_time,
    "total_hours": round(total_time / 60, 2),
    "tasks": [{"task": k, "total_minutes": v["total_minutes"], "entry_count": v["count"], "hours": round(v["total_minutes"]/60, 2)} for k, v in task_totals.items()],
    "generated_at": datetime.now().isoformat()
}

with open(SUMMARY_FILE, 'w') as f:
    json.dump([summary], f, indent=2)

print(f"[OK] Total time: {summary['total_hours']} hours")
print(f"[OK] Unique tasks: {summary['total_tasks']}")

# Step 3: Generate charts using visualization module
print("\n[3/3] Generating dashboard charts...")

# Pie chart
result1 = create_task_distribution_chart(
    tasks, 
    PIE_FILE, 
    f"Time Distribution - {today}"
)
if result1:
    print("[OK] Created task_distribution.png")

# Timeline chart
result2 = create_daily_timeline_chart(
    tasks,
    TIMELINE_FILE,
    f"Task Timeline - {today}"
)
if result2:
    print("[OK] Created daily_timeline.png")

# Weekly summary
result3 = create_weekly_summary_chart([summary], WEEKLY_FILE, "Weekly Time Tracking Summary")
if result3:
    print("[OK] Created weekly_summary.png")

print("\n" + "="*50)
print("*** TEST COMPLETE! ***")
print("="*50)
print("\nGenerated files:")
print("  - tasks.json (raw data)")
print("  - daily_summary.json (summary)")
print("  - task_distribution.png (pie chart)")
print("  - daily_timeline.png (timeline)")
print("  - weekly_summary.png (weekly chart)")