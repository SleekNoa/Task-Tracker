"""
Application Configuration
"""

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
TIMERS_FILE = os.path.join(DATA_DIR, "timers.json")
WORK_SESSIONS_FILE = os.path.join(DATA_DIR, "work_sessions.json")
SUMMARIES_FILE = os.path.join(DATA_DIR, "summaries.json")

SERVER_PORT = 8765
SERVER_HOST = "localhost"

os.makedirs(DATA_DIR, exist_ok=True)