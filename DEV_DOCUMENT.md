# Software Development Document - Task Tracker

## Project Overview
**Project Name:** Task Tracker  
**Purpose:** Desktop application that pops up at intervals asking "What are you working on?" and generates daily time summaries.

---

## 1. Requirements

### Functional Requirements
- [ ] Popup dialog at configurable intervals (default: 60 minutes)
- [ ] Task description input with submit/skip options
- [ ] Local JSON storage for all task entries
- [ ] Daily summary report generation
- [ ] Dashboard visualization with charts
- [ ] End-of-day notification with total time tally

### Non-Functional Requirements
- [x] Windows-only support
- [x] Offline-first operation
- [x] JSON output for NoSQL compatibility
- [ ] Simple deployment (executable or script)

---

## 2. Architecture

### Components
| Component | File | Description |
|-----------|------|-------------|
| Main App | `task_tracker.py` | Popup timer and task collection |
| Storage | `tasks.json` | Local JSON database |
| Summary | `summary_report.py` | Daily report generator |
| Dashboard | `dashboard.py` | Visualization charts |

### Data Flow
```
[Popup Timer] → [Task Entry] → tasks.json → [Summary Report] → daily_summary.json
                                      └─→ [Dashboard Charts]
```

---

## 3. Data Schema

### Task Entry (tasks.json)
```json
{
  "timestamp": "2026-09-25T11:30:00",
  "date": "2026-09-25",
  "time": "11:30:00",
  "task": "Working on Task Tracker app",
  "duration_minutes": 60
}
```

### Daily Summary (daily_summary.json)
```json
{
  "date": "2026-09-25",
  "total_tasks": 5,
  "total_time_minutes": 300,
  "total_hours": 5.0,
  "tasks": [
    {
      "task": "Task description",
      "total_minutes": 120,
      "entry_count": 2,
      "hours": 2.0
    }
  ]
}
```

---

## 4. Development Progress

### Sprint 1 - Core Functionality
- [x] Create project structure
- [x] Build popup timer component
- [x] Implement JSON storage
- [x] Create summary report generator
- [x] Add dashboard visualization

### Sprint 2 - Enhancements
- [ ] Configurable interval settings
- [ ] End-of-day automatic summary
- [ ] Task categories/tags
- [ ] Export to CSV/Excel

### Sprint 3 - Deployment
- [ ] Create standalone executable
- [ ] Add system tray icon
- [ ] Auto-start on Windows login
- [ ] Installable package

---

## 5. Testing Checklist

### Unit Tests
- [ ] Popup appears at correct intervals
- [ ] Task data saves correctly to JSON
- [ ] Summary calculation is accurate
- [ ] Charts generate without errors

### Manual Tests
- [ ] Run app for full day
- [ ] Verify end-of-day summary
- [ ] Check chart accuracy

---

## 6. Future Considerations

### NoSQL Migration Path
- MongoDB: Direct JSON import
- SQL Server: JSON column support
- CosmosDB: Document storage

### Enterprise Features
- [ ] Teams/Outlook integration
- [ ] Corporate LDAP authentication
- [ ] Centralized reporting endpoint

---

## 7. Notes & Decisions

**2026-09-25** - Initial prototype created using Python/tkinter for simplicity and Windows compatibility. JSON storage chosen for easy NoSQL migration later.

---

## 8. Commands

### Install Dependencies
```powershell
C:\Users\e40057804\Downloads\python-portable-new\python.exe -m pip install matplotlib seaborn
```

### Quick Test (No Popup)
```powershell
cd C:\Users\e40057804\AppData\Local\poolside\scratch\task-tracker
C:\Users\e40057804\Downloads\python-portable-new\python.exe quick_test.py
```

### Run Task Tracker
```powershell
cd C:\Users\e40057804\AppData\Local\poolside\scratch\task-tracker
C:\Users\e40057804\Downloads\python-portable-new\python.exe task_tracker.py
```

### Generate Summary
```powershell
C:\Users\e40057804\Downloads\python-portable-new\python.exe summary_report.py
```

### Generate Dashboard
```powershell
C:\Users\e40057804\Downloads\python-portable-new\python.exe dashboard.py
```