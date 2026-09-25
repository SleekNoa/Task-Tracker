"""
Visualization Module for Task Tracker
Generates charts from task data.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict

def create_task_distribution_chart(tasks, output_file="task_distribution.png", title="Time Distribution"):
    """Create a pie chart showing time distribution across tasks."""
    if not tasks:
        return None
    
    # Aggregate by task
    task_totals = defaultdict(float)
    for task in tasks:
        task_desc = task.get("task", "Unknown")
        duration = task.get("duration_minutes", 60)
        task_totals[task_desc] += duration
    
    # Create pie chart
    labels = list(task_totals.keys())
    sizes = list(task_totals.values())
    
    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_file, dpi=100)
    plt.close()
    
    return output_file


def create_daily_timeline_chart(tasks, output_file="daily_timeline.png", title="Task Timeline"):
    """Create a horizontal bar chart showing tasks throughout the day."""
    if not tasks:
        return None
    
    # Sort by time
    sorted_tasks = sorted(tasks, key=lambda x: x.get("time", "00:00:00"))
    
    # Create timeline
    plt.figure(figsize=(12, 6))
    
    times = [t.get("time", "00:00")[:5] for t in sorted_tasks]
    durations = [t.get("duration_minutes", 60) for t in sorted_tasks]
    labels = [t.get("task", "Unknown")[:25] for t in sorted_tasks]
    
    y_pos = range(len(times))
    plt.barh(y_pos, durations, align='center', color='#3498db')
    plt.yticks(y_pos, labels)
    plt.xlabel('Duration (minutes)')
    plt.title(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=100)
    plt.close()
    
    return output_file


def create_weekly_summary_chart(summaries, output_file="weekly_summary.png", title="Weekly Summary"):
    """Create a bar chart showing total time per day for the last 7 days."""
    if not summaries:
        return None
    
    # Get last 7 days
    dates = []
    hours = []
    
    for summary in sorted(summaries, key=lambda x: x.get("date", ""), reverse=True)[:7]:
        dates.append(summary.get("date", "Unknown"))
        hours.append(summary.get("total_hours", 0))
    
    # Reverse for chronological order
    dates = dates[::-1]
    hours = hours[::-1]
    
    plt.figure(figsize=(10, 5))
    plt.bar(dates, hours, color='#27ae60')
    plt.xlabel('Date')
    plt.ylabel('Hours')
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=100)
    plt.close()
    
    return output_file