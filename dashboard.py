"""
Dashboard Visualization Script
Generates charts and visualizations from task data using matplotlib.
"""

import json
import os
from datetime import datetime
from visualization import create_task_distribution_chart, create_daily_timeline_chart, create_weekly_summary_chart

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


def load_summaries():
    """Load summary reports"""
    if os.path.exists(REPORT_FILE):
        try:
            with open(REPORT_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []


def generate_task_distribution_chart(target_date=None, output_file="task_distribution.png"):
    """Generate a pie chart showing time distribution across tasks."""
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    
    tasks = load_tasks()
    daily_tasks = [t for t in tasks if t.get("date") == target_date]
    
    if not daily_tasks:
        print(f"No tasks found for {target_date}")
        return None
    
    result = create_task_distribution_chart(
        daily_tasks, 
        output_file, 
        f"Time Distribution - {target_date}"
    )
    if result:
        print(f"Chart saved to {output_file}")
    return result


def generate_daily_timeline_chart(target_date=None, output_file="daily_timeline.png"):
    """Generate a horizontal bar chart showing tasks throughout the day."""
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    
    tasks = load_tasks()
    daily_tasks = [t for t in tasks if t.get("date") == target_date]
    
    if not daily_tasks:
        print(f"No tasks found for {target_date}")
        return None
    
    result = create_daily_timeline_chart(
        daily_tasks,
        output_file,
        f"Task Timeline - {target_date}"
    )
    if result:
        print(f"Chart saved to {output_file}")
    return result


def generate_weekly_summary_chart(output_file="weekly_summary.png"):
    """Generate a bar chart showing total time per day for the last 7 days."""
    summaries = load_summaries()
    
    if not summaries:
        print("No summary data available")
        return None
    
    result = create_weekly_summary_chart(summaries, output_file, "Weekly Time Tracking Summary")
    if result:
        print(f"Chart saved to {output_file}")
    return result


def generate_dashboard(target_date=None):
    """Generate all dashboard charts for a specific date."""
    print("\nGenerating Dashboard Charts...")
    print("="*40)
    
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    
    charts = []
    
    chart1 = generate_task_distribution_chart(target_date)
    if chart1:
        charts.append(chart1)
    
    chart2 = generate_daily_timeline_chart(target_date)
    if chart2:
        charts.append(chart2)
    
    chart3 = generate_weekly_summary_chart()
    if chart3:
        charts.append(chart3)
    
    print("\nDashboard generation complete!")
    print(f"Generated {len(charts)} charts")
    
    return charts


def main():
    """Generate dashboard for today"""
    generate_dashboard()


if __name__ == "__main__":
    main()