import subprocess
import time
import sys
import os
import signal
import urllib.request

def kill_processes(name):
    try:
        subprocess.run(["taskkill", "/f", "/im", name], capture_output=True, check=False)
    except Exception:
        pass

print("Stopping old services...")
kill_processes("python.exe")
kill_processes("node.exe")
time.sleep(2)

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(root, "backend")
frontend_dir = os.path.join(root, "frontend")

backend_log = open(os.path.join(backend_dir, "server.log"), "w")
frontend_log = open(os.path.join(frontend_dir, "server.log"), "w")

env = os.environ.copy()
env["PYTHONPATH"] = backend_dir

print("Starting backend...")
backend_proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=backend_dir,
    env=env,
    stdout=backend_log,
    stderr=subprocess.STDOUT,
)

time.sleep(4)

print("Starting frontend...")
frontend_proc = subprocess.Popen(
    ["npm", "run", "dev"],
    cwd=frontend_dir,
    stdout=frontend_log,
    stderr=subprocess.STDOUT,
)

time.sleep(6)

backend_ok = False
frontend_ok = False

try:
    r = urllib.request.urlopen("http://localhost:8000/api/matches/live", timeout=5)
    print(f"BACKEND OK (pid={backend_proc.pid}) status={r.status}")
    backend_ok = True
except Exception as e:
    print(f"BACKEND ERROR: {e}")

try:
    r = urllib.request.urlopen("http://localhost:3000", timeout=5)
    print(f"FRONTEND OK (pid={frontend_proc.pid}) status={r.status}")
    frontend_ok = True
except Exception as e:
    print(f"FRONTEND ERROR: {e}")

if backend_ok and frontend_ok:
    print("\nAll services are running!")
    print("Backend:  http://localhost:8000")
    print("Frontend: http://localhost:3000")
    print("Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        backend_proc.terminate()
        frontend_proc.terminate()
        backend_log.close()
        frontend_log.close()
else:
    print("\nSome services failed to start.")
    backend_proc.terminate()
    frontend_proc.terminate()
    backend_log.close()
    frontend_log.close()
