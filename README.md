# Task Tracker - SPA Web Dashboard

**Original Idea:** "Pops up at set intervals asking what you're working on, then sends a daily tally of time spent"

## ✅ **SINGLE PAGE APPLICATION (SPA) ARCHITECTURE**

### **How to Run (Double-click)**
- **Double-click `RUN_TASK_TRACKER.bat`**
- Your web browser opens with the Task Tracker dashboard

---

## **SPA Pages**

| Page | URL | Purpose |
|------|-----|---------|
| **Tracker** | `/tracker` | Add tasks, start/stop timers |
| **Summary** | `/summary` | Daily time breakdown |
| **Visualization** | `/visualization` | Charts & graphs page |

---

## **Tracker Page Features**

### 1. **Hourly Task Entry**
- Type what you worked on
- Counts as 60 minutes
- Quick logging

### 2. **Timed Task Tracking** ✅ NEW
- **Start Timer** - Begin tracking actual time
- **Stop Timer** - Stops and records exact minutes
- Shows live timer (mm:ss) while running
- Records precise duration

### 3. **Today's Tasks List**
- Shows all tasks with time and duration

---

## **Example Usage**

1. **Quick entry:** Type "Email responses" → Click "Add Task" → Records 60 min

2. **Timed tracking:** 
   - Type "Feature development" → Click "Start Timer"
   - Work for 45 minutes
   - Click "Stop Timer" → Records 45 min exactly

---

## **Data Files**

| File | Purpose |
|------|---------|
| `tasks.json` | Raw task log with type field |
| `dashboard.html` | Generated HTML |

---

## **Project Location**
```
C:\Users\e40057804\task-tracker
```

---

## **Project Structure**
```
task-tracker/
├── RUN_TASK_TRACKER.bat    # Main SPA app
├── RUN_QUICK_TEST.bat      # Test with sample data
├── web_dashboard.py        # SPA server (MAIN APP)
├── task_tracker.py         # Console version (backup)
├── summary_report.py       # Daily summary generator
├── dashboard.py            # Chart generator
├── visualization.py        # Chart functions
├── tasks.json              # Your task data
└── tests/
    └── quick_test.py       # Test script
```