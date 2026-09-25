"""
Report Service
"""

from typing import List, Dict
from collections import defaultdict
from datetime import datetime
from app.storage.json_storage import JSONStorage
from app.config import TASKS_FILE, SUMMARIES_FILE


class ReportService:
    """Application service for report generation."""
    
    def __init__(self):
        self.tasks_storage = JSONStorage(TASKS_FILE)
        self.summaries_storage = JSONStorage(SUMMARIES_FILE)
    
    def get_daily_summary(self, target_date: str = None) -> Dict:
        """Generate daily summary for a specific date."""
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")
        
        records = self.tasks_storage.read()
        daily_tasks = [t for t in records if t.get("date") == target_date]
        
        if not daily_tasks:
            return {
                "date": target_date,
                "total_tasks": 0,
                "total_time_minutes": 0,
                "total_hours": 0,
                "tasks": []
            }
        
        task_totals = defaultdict(lambda: {"count": 0, "total_minutes": 0})
        for task in daily_tasks:
            task_desc = task.get("task", "Unknown")
            duration = task.get("duration_minutes", 60)
            task_totals[task_desc]["count"] += 1
            task_totals[task_desc]["total_minutes"] += duration
        
        total_minutes = sum(item["total_minutes"] for item in task_totals.values())
        
        tasks_list = []
        for task_desc, data in task_totals.items():
            tasks_list.append({
                "task": task_desc,
                "total_minutes": data["total_minutes"],
                "entry_count": data["count"],
                "hours": round(data["total_minutes"] / 60, 2)
            })
        
        tasks_list.sort(key=lambda x: x["total_minutes"], reverse=True)
        
        return {
            "date": target_date,
            "total_tasks": len(tasks_list),
            "total_time_minutes": total_minutes,
            "total_hours": round(total_minutes / 60, 2),
            "tasks": tasks_list
        }
    
    def get_weekly_summary(self, days: int = 7) -> List[Dict]:
        """Get summaries for the last N days."""
        summaries = []
        for i in range(days):
            date = datetime.now()
            # Would need date arithmetic for real implementation
            summary = self.get_daily_summary()
            summaries.append(summary)
        return summaries
    
    def save_summary(self, summary: Dict):
        """Save summary to summaries file."""
        summaries = self.summaries_storage.read()
        summaries = [s for s in summaries if s.get("date") != summary["date"]]
        summaries.append(summary)
        summaries.sort(key=lambda x: x.get("date", ""), reverse=True)
        self.summaries_storage.write(summaries)