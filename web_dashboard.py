"""
Task Tracker SPA - Single Page Application with Persistent Timer
Timer continues even when navigating away from the page.
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

DATA_FILE = "tasks.json"
PORT = 8765

class TaskHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/tracker":
            self.serve_tracker()
        elif self.path == "/summary":
            self.serve_summary()
        elif self.path == "/visualization":
            self.serve_visualization()
        elif self.path == "/api/tasks":
            self.serve_tasks_json()
        elif self.path == "/api/summary":
            self.serve_summary_json()
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == "/api/add-task":
            self.handle_add_task()
        elif self.path == "/api/start-task":
            self.handle_start_task()
        elif self.path == "/api/stop-task":
            self.handle_stop_task()
        elif self.path == "/api/check-timer":
            self.handle_check_timer()
        else:
            self.send_error(404)
    
    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self, tasks):
        with open(DATA_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)
    
    def handle_add_task(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        task_text = data.get('task', '').strip()
        if task_text:
            tasks = self.load_tasks()
            entry = {
                "timestamp": datetime.now().isoformat(),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M"),
                "task": task_text,
                "duration_minutes": 60,
                "type": "hourly"
            }
            tasks.append(entry)
            self.save_tasks(tasks)
        
        self.send_json_response({"status": "ok"})
    
    def handle_start_task(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        task_text = data.get('task', '').strip()
        if task_text:
            # Save timer start to file
            timer_data = {
                "task": task_text,
                "start_time": time.time(),
                "active": True
            }
            with open("timer_state.json", 'w') as f:
                json.dump(timer_data, f)
        
        self.send_json_response({"status": "ok", "active_task": task_text})
    
    def handle_stop_task(self):
        if os.path.exists("timer_state.json"):
            with open("timer_state.json", 'r') as f:
                timer_data = json.load(f)
            
            if timer_data.get("active"):
                start_time = timer_data.get("start_time", time.time())
                elapsed_seconds = time.time() - start_time
                elapsed_minutes = max(1, round(elapsed_seconds / 60))
                
                tasks = self.load_tasks()
                entry = {
                    "timestamp": datetime.now().isoformat(),
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M"),
                    "task": timer_data.get("task", "Unknown"),
                    "duration_minutes": elapsed_minutes,
                    "type": "timed"
                }
                tasks.append(entry)
                self.save_tasks(tasks)
                
                # Clear timer state
                os.remove("timer_state.json")
        
        self.send_json_response({"status": "ok"})
    
    def handle_check_timer(self):
        if os.path.exists("timer_state.json"):
            with open("timer_state.json", 'r') as f:
                timer_data = json.load(f)
            
            if timer_data.get("active"):
                elapsed_seconds = time.time() - timer_data.get("start_time", time.time())
                self.send_json_response({
                    "active": True,
                    "task": timer_data.get("task"),
                    "elapsed_seconds": elapsed_seconds
                })
            else:
                self.send_json_response({"active": False})
        else:
            self.send_json_response({"active": False})
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_html_response(self, html):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_tracker(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Task Tracker - Tracker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #2c3e50; color: white; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { text-align: center; }
        .nav { text-align: center; margin: 20px 0; }
        .nav a { color: #3498db; margin: 0 10px; text-decoration: none; }
        .section { background: white; color: black; padding: 20px; border-radius: 10px; margin: 20px 0; }
        h2 { margin-top: 0; color: #2c3e50; }
        input, button { padding: 10px; font-size: 14px; }
        input { width: 70%; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2ecc71; }
        .timer-section { background: #f39c12; color: white; }
        .timer-active { background: #27ae60; }
        #timerDisplay { font-size: 24px; font-weight: bold; margin: 10px 0; }
        #activeTaskName { font-weight: bold; margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Task Tracker</h1>
        <div class="nav">
            <a href="/tracker">Tracker</a> | 
            <a href="/summary">Summary</a> | 
            <a href="/visualization">Visualization</a>
        </div>
        
        <div class="section">
            <h2>Add Hourly Task</h2>
            <p>Record what you worked on (counts as 60 minutes)</p>
            <input type="text" id="hourlyTask" placeholder="What did you work on this hour?">
            <button onclick="addHourlyTask()">Add Task</button>
            <p id="status1" style="color: green; margin-top: 10px;"></p>
        </div>
        
        <div class="section timer-section" id="timerSection">
            <h2>Timed Task Tracking</h2>
            <p>Track actual time spent on a task</p>
            <div id="activeTaskName"></div>
            <input type="text" id="timedTask" placeholder="What are you starting work on?">
            <button onclick="startTimedTask()" id="startBtn">Start Timer</button>
            <button onclick="stopTimedTask()" id="stopBtn" style="display:none;">Stop Timer</button>
            <div id="timerDisplay"></div>
            <p id="status2" style="color: yellow;"></p>
        </div>
        
        <div class="section">
            <h2>Today's Tasks</h2>
            <div id="tasksList">Loading...</div>
            <button onclick="loadTasks()">Refresh</button>
        </div>
    </div>
    
    <script>
        let timerInterval = null;
        let startTime = null;
        let activeTask = null;
        
        // Check for existing timer on page load
        async function checkTimer() {
            const response = await fetch('/api/check-timer');
            const data = await response.json();
            if (data.active) {
                activeTask = data.task;
                startTime = Date.now() - (data.elapsed_seconds * 1000);
                document.getElementById('activeTaskName').textContent = 'Active: ' + activeTask;
                document.getElementById('timedTask').value = activeTask;
                document.getElementById('startBtn').style.display = 'none';
                document.getElementById('stopBtn').style.display = 'inline-block';
                document.getElementById('timerSection').className = 'section timer-active';
                updateTimer();
                timerInterval = setInterval(updateTimer, 1000);
            }
        }
        
        async function startTimedTask() {
            const task = document.getElementById('timedTask').value.trim();
            if (task) {
                const response = await fetch('/api/start-task', {
                    method: 'POST',
                    body: JSON.stringify({task: task}),
                    headers: {'Content-Type': 'application/json'}
                });
                const data = await response.json();
                activeTask = data.active_task;
                startTime = Date.now();
                document.getElementById('activeTaskName').textContent = 'Active: ' + activeTask;
                document.getElementById('startBtn').style.display = 'none';
                document.getElementById('stopBtn').style.display = 'inline-block';
                document.getElementById('timerSection').className = 'section timer-active';
                updateTimer();
                timerInterval = setInterval(updateTimer, 1000);
            }
        }
        
        async function stopTimedTask() {
            const response = await fetch('/api/stop-task', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });
            clearInterval(timerInterval);
            activeTask = null;
            startTime = null;
            document.getElementById('activeTaskName').textContent = '';
            document.getElementById('startBtn').style.display = 'inline-block';
            document.getElementById('stopBtn').style.display = 'none';
            document.getElementById('timerSection').className = 'section timer-section';
            document.getElementById('timerDisplay').textContent = '';
            loadTasks();
        }
        
        function updateTimer() {
            if (startTime) {
                const elapsed = Math.floor((Date.now() - startTime) / 1000);
                const mins = Math.floor(elapsed / 60);
                const secs = elapsed % 60;
                document.getElementById('timerDisplay').textContent = 
                    mins.toString().padStart(2, '0') + ':' + secs.toString().padStart(2, '0');
            }
        }
        
        async function loadTasks() {
            const response = await fetch('/api/tasks');
            const tasks = await response.json();
            const today = new Date().toISOString().split('T')[0];
            const todayTasks = tasks.filter(t => t.date === today);
            let html = '<table style="width:100%; border-collapse:collapse;"><tr><th>Time</th><th>Task</th><th>Duration</th><th>Type</th></tr>';
            todayTasks.slice(-10).reverse().forEach(t => {
                html += `<tr><td>${t.time}</td><td>${t.task}</td><td>${t.duration_minutes}m</td><td>${t.type || 'hourly'}</td></tr>`;
            });
            html += '</table>';
            document.getElementById('tasksList').innerHTML = html;
        }
        
        async function addHourlyTask() {
            const task = document.getElementById('hourlyTask').value.trim();
            if (task) {
                await fetch('/api/add-task', {
                    method: 'POST',
                    body: JSON.stringify({task: task}),
                    headers: {'Content-Type': 'application/json'}
                });
                document.getElementById('hourlyTask').value = '';
                document.getElementById('status1').textContent = 'Task added!';
                setTimeout(() => document.getElementById('status1').textContent = '', 2000);
                loadTasks();
            }
        }
        
        // Initialize
        checkTimer();
        loadTasks();
        
        document.getElementById('hourlyTask').addEventListener('keydown', e => { if(e.key==='Enter') addHourlyTask(); });
        document.getElementById('timedTask').addEventListener('keydown', e => { if(e.key==='Enter') startTimedTask(); });
    </script>
</body>
</html>"""
        self.send_html_response(html)
    
    def serve_summary(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Task Tracker - Summary</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #2c3e50; color: white; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { text-align: center; }
        .nav { text-align: center; margin: 20px 0; }
        .nav a { color: #3498db; margin: 0 10px; text-decoration: none; }
        .section { background: white; color: black; padding: 20px; border-radius: 10px; margin: 20px 0; }
        h2 { margin-top: 0; color: #2c3e50; }
        .card { display: inline-block; padding: 15px 25px; margin: 5px; border-radius: 8px; color: white; font-weight: bold; }
        .total { background: #3498db; }
        .tasks { background: #2ecc71; }
        .date { background: #9b59b6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Task Tracker</h1>
        <div class="nav">
            <a href="/tracker">Tracker</a> | 
            <a href="/summary">Summary</a> | 
            <a href="/visualization">Visualization</a>
        </div>
        
        <div id="summaryContent">Loading...</div>
    </div>
    
    <script>
        async function loadSummary() {
            const response = await fetch('/api/summary');
            const data = await response.json();
            const today = data[0] || {};
            let html = `
            <div class="section">
                <h2>Today's Summary</h2>
                <div class="cards">
                    <div class="card total">Total: ${today.total_hours || 0}h (${today.total_time_minutes || 0}m)</div>
                    <div class="card tasks">Tasks: ${today.total_tasks || 0}</div>
                    <div class="card date">Date: ${today.date || 'N/A'}</div>
                </div>
                <h3>Task Breakdown</h3>
                <table style="width:100%; border-collapse:collapse;"><tr><th>#</th><th>Task</th><th>Minutes</th><th>Hours</th></tr>
            `;
            (today.tasks || []).forEach((t, i) => {
                html += `<tr><td>${i+1}</td><td>${t.task}</td><td>${t.total_minutes}</td><td>${t.hours}</td></tr>`;
            });
            html += '</table></div>';
            document.getElementById('summaryContent').innerHTML = html;
        }
        loadSummary();
    </script>
</body>
</html>"""
        self.send_html_response(html)
    
    def serve_visualization(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Task Tracker - Visualization</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #2c3e50; color: white; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { text-align: center; }
        .nav { text-align: center; margin: 20px 0; }
        .nav a { color: #3498db; margin: 0 10px; text-decoration: none; }
        .section { background: white; color: black; padding: 20px; border-radius: 10px; margin: 20px 0; }
        h2 { margin-top: 0; color: #2c3e50; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Task Tracker</h1>
        <div class="nav">
            <a href="/tracker">Tracker</a> | 
            <a href="/summary">Summary</a> | 
            <a href="/visualization">Visualization</a>
        </div>
        
        <div class="section">
            <h2>Charts & Visualizations</h2>
            <p>Run the visualization script to generate charts:</p>
            <ul>
                <li><strong>task_distribution.png</strong> - Pie chart of time by task</li>
                <li><strong>daily_timeline.png</strong> - Bar chart of tasks throughout the day</li>
                <li><strong>weekly_summary.png</strong> - Bar chart of hours per day</li>
            </ul>
            <p>Charts are generated by running: <code>python dashboard.py</code></p>
        </div>
    </div>
</body>
</html>"""
        self.send_html_response(html)
    
    def serve_tasks_json(self):
        tasks = self.load_tasks()
        self.send_json_response(tasks)
    
    def serve_summary_json(self):
        tasks = self.load_tasks()
        today = datetime.now().strftime("%Y-%m-%d")
        daily_tasks = [t for t in tasks if t.get("date") == today]
        
        task_totals = defaultdict(lambda: {"count": 0, "total_minutes": 0})
        for task in daily_tasks:
            task_totals[task["task"]]["count"] += 1
            task_totals[task["task"]]["total_minutes"] += task.get("duration_minutes", 60)
        
        total_minutes = sum(v["total_minutes"] for v in task_totals.values())
        
        summary = {
            "date": today,
            "total_tasks": len(task_totals),
            "total_time_minutes": total_minutes,
            "total_hours": round(total_minutes / 60, 1),
            "tasks": [{"task": k, "total_minutes": v["total_minutes"], "hours": round(v["total_minutes"]/60, 1)} for k, v in task_totals.items()]
        }
        
        self.send_json_response([summary])
    
    def log_message(self, format, *args):
        pass

def run_server():
    server = HTTPServer(('localhost', PORT), TaskHandler)
    server.serve_forever()

def main():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    url = f"http://localhost:{PORT}/tracker"
    webbrowser.open(url)
    
    print("="*50)
    print("TASK TRACKER - SPA Web Dashboard")
    print("="*50)
    print(f"\nDashboard: {url}")
    print("\nNavigation:")
    print("  /tracker         - Add tasks and track time")
    print("  /summary         - View daily summary")
    print("  /visualization   - Charts page")
    print("\nTimer persists across page navigation!")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()