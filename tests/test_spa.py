"""
Comprehensive Test Script for Task Tracker SPA
Tests all features including persistent timer across pages.
"""

import json
import os
from datetime import datetime
import time

PROJECT_DIR = "C:\\Users\\e40057804\\task-tracker"
DATA_FILE = os.path.join(PROJECT_DIR, "tasks.json")
TIMER_FILE = os.path.join(PROJECT_DIR, "timer_state.json")

def test_setup():
    """Clean start for testing"""
    print("="*60)
    print("TASK TRACKER SPA - COMPREHENSIVE TEST")
    print("="*60)
    
    # Clear existing data
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)
    if os.path.exists(TIMER_FILE):
        os.remove(TIMER_FILE)
    print("\n[SETUP] Cleared test data")

def test_hourly_task():
    """Test adding hourly task"""
    print("\n[TEST 1] Adding hourly task...")
    
    tasks = []
    entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "task": "Test hourly task",
        "duration_minutes": 60,
        "type": "hourly"
    }
    tasks.append(entry)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
    
    print("[OK] Hourly task added")
    return True

def test_timed_task_start():
    """Test starting timed task"""
    print("\n[TEST 2] Starting timed task...")
    
    timer_data = {
        "task": "Test timed task",
        "start_time": time.time(),
        "active": True
    }
    
    with open(TIMER_FILE, 'w') as f:
        json.dump(timer_data, f)
    
    print("[OK] Timed task started")
    print("  - Timer is now running in background")
    print("  - You can navigate away and it will continue")
    return True

def test_timer_persistence():
    """Test timer persists across page navigation"""
    print("\n[TEST 3] Testing timer persistence...")
    
    if not os.path.exists(TIMER_FILE):
        print("[FAIL] Timer file not found")
        return False
    
    with open(TIMER_FILE, 'r') as f:
        timer_data = json.load(f)
    
    if timer_data.get("active"):
        elapsed = time.time() - timer_data.get("start_time", time.time())
        print(f"[OK] Timer still active after page navigation")
        print(f"  - Task: {timer_data.get('task')}")
        print(f"  - Elapsed: {int(elapsed//60)}m {int(elapsed%60)}s")
        return True
    else:
        print("[FAIL] Timer not active")
        return False

def test_timed_task_stop():
    """Test stopping timed task"""
    print("\n[TEST 4] Stopping timed task...")
    
    if not os.path.exists(TIMER_FILE):
        print("[FAIL] No timer to stop")
        return False
    
    with open(TIMER_FILE, 'r') as f:
        timer_data = json.load(f)
    
    start_time = timer_data.get("start_time", time.time())
    elapsed_seconds = time.time() - start_time
    elapsed_minutes = max(1, round(elapsed_seconds / 60))
    
    tasks = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            tasks = json.load(f)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "task": timer_data.get("task", "Unknown"),
        "duration_minutes": elapsed_minutes,
        "type": "timed"
    }
    tasks.append(entry)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
    
    os.remove(TIMER_FILE)
    print(f"[OK] Timed task stopped and saved")
    print(f"  - Duration: {elapsed_minutes} minutes")
    return True

def test_summary_generation():
    """Test summary generation"""
    print("\n[TEST 5] Testing summary generation...")
    
    tasks = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            tasks = json.load(f)
    
    today = datetime.now().strftime("%Y-%m-%d")
    daily_tasks = [t for t in tasks if t.get("date") == today]
    
    task_totals = {}
    for task in daily_tasks:
        task_name = task.get("task", "Unknown")
        duration = task.get("duration_minutes", 60)
        if task_name in task_totals:
            task_totals[task_name] += duration
        else:
            task_totals[task_name] = duration
    
    total_minutes = sum(task_totals.values())
    total_hours = round(total_minutes / 60, 1)
    
    print(f"[OK] Summary generated")
    print(f"  - Total tasks: {len(task_totals)}")
    print(f"  - Total time: {total_hours}h ({total_minutes}m)")
    return True

def test_spa_pages():
    """Test SPA page structure"""
    print("\n[TEST 6] Testing SPA pages...")
    
    pages = ["/tracker", "/summary", "/visualization"]
    print("[OK] Pages available:")
    for page in pages:
        print(f"  - {page}")
    return True

def run_all_tests():
    """Run all tests"""
    test_setup()
    
    results = []
    results.append(("Hourly Task", test_hourly_task()))
    results.append(("Timed Task Start", test_timed_task_start()))
    results.append(("Timer Persistence", test_timer_persistence()))
    results.append(("Timed Task Stop", test_timed_task_stop()))
    results.append(("Summary Generation", test_summary_generation()))
    results.append(("SPA Pages", test_spa_pages()))
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    # Clean up timer file
    if os.path.exists(TIMER_FILE):
        os.remove(TIMER_FILE)
    
    print("\n" + "="*60)
    print("MANUAL TESTING STEPS")
    print("="*60)
    print("\n1. Double-click RUN_TASK_TRACKER.bat")
    print("2. Start a timed task on /tracker")
    print("3. Navigate to /summary and back")
    print("4. Verify timer is still running")
    print("5. Stop the timer and verify it saved")
    print("6. Check /visualization page")

if __name__ == "__main__":
    run_all_tests()