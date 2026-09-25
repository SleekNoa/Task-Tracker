# Task Tracker - SPA Web Dashboard

**Original Idea:** "Pops up at set intervals asking what you're working on, then sends a daily tally of time spent"

---

## 📋 Version History

| Version | Branch | Description |
|---------|--------|-------------|
| v1.0 | `main` | Original prototype with embedded business logic |
| v2.0 | `architecture-refactor` | Layered architecture with clean separation of concerns |

---

## ✅ **CURRENT VERSION: Layered Architecture (v2.0)**

The application has been refactored to follow Clean Architecture / Hexagonal Architecture principles.

### Architecture Overview
```
                 WEB UI / CLI
                     │
                     ▼
               HTTP Handlers
                     │
                     ▼
            APPLICATION SERVICES
                     │
            ┌────────┼────────┐
            │        │        │
            ▼        ▼        ▼
         Task    Timer     Report
            │        │        │
            └────────┼────────┘
                     ▼
                  DOMAIN
                     │
                     ▼
                REPOSITORIES
                     │
                     ▼
                JSON STORAGE
```

### How to Run (Double-click)
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

### 2. **Timed Task Tracking**
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

| File | Location | Purpose |
|------|----------|---------|
| `tasks.json` | `data/` | Raw task log with type field |
| `timers.json` | `data/` | Active timer state |
| `work_sessions.json` | `data/` | Completed work sessions |
| `summaries.json` | `data/` | Generated daily summaries |

---

## **Project Location**
```
C:\Users\e40057804\task-tracker
```

---

## **Project Structure (v2.0)**

```
task-tracker/
├── RUN_TASK_TRACKER.bat          # Main SPA app launcher
├── RUN_QUICK_TEST.bat            # Test with sample data
├── web_dashboard.py            # Web interface (HTTP adapter)
├── task_tracker.py               # CLI entry point
│
├── app/                        # Application core
│   ├── domain/                 # Domain models
│   │   ├── task.py
│   │   ├── timer.py
│   │   └── work_session.py
│   │
│   ├── services/               # Application services
│   │   ├── task_service.py
│   │   ├── timer_service.py
│   │   └── report_service.py
│   │
│   ├── repositories/           # Data access
│   │   ├── task_repository.py
│   │   ├── timer_repository.py
│   │   └── work_session_repository.py
│   │
│   └── storage/                # Persistence
│       └── json_storage.py
│
├── interfaces/                 # External interfaces
│   └── cli/
│       └── main.py
│
├── data/                       # JSON data files
│   ├── tasks.json
│   ├── timers.json
│   ├── work_sessions.json
│   └── summaries.json
│
├── visualization/              # Chart generation
│   └── charts.py
│
└── tests/                      # Test suite
    ├── domain/
    ├── services/
    └── integration/
```

---

## **Running Tests**

```bash
# Domain model tests
python tests/domain/test_models.py

# Service tests
python tests/services/test_services.py

# Quick test with sample data
RUN_QUICK_TEST.bat
```

---

## **Architecture Benefits**

| Feature | v1.0 (Prototype) | v2.0 (Refactored) |
|---------|------------------|-------------------|
| Business Logic | Mixed with HTTP handlers | Isolated in services |
| Data Access | Scattered across files | Centralized in repositories |
| Domain Models | None | Task, Timer, WorkSession |
| Testability | Manual JSON manipulation | Service-level tests |
| Extensibility | Low | High |
| Multiple UIs | Hard to add | Easy (Web + CLI share services) |

---

## **Git Branches**

```bash
# View original prototype
git checkout main

# View refactored architecture
git checkout architecture-refactor
```

---

## **Future Roadmap**

- [ ] Add SQLite repository implementation
- [ ] Add authentication layer
- [ ] Add REST API endpoints
- [ ] Create mobile interface
- [ ] Add project tracking features
- [ ] Add habit tracking features