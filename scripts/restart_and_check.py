import subprocess
import sys
import time
import urllib.request

# Kill old processes
try:
    subprocess.run(["taskkill", "/f", "/im", "python.exe"], capture_output=True, check=False)
except Exception:
    pass
time.sleep(2)

backend_dir = r"D:\vs code\sait\backend"
env = {"PYTHONPATH": backend_dir}
env.update({k: v for k, v in __import__('os').environ.items() if k not in env})

proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=backend_dir,
    env=env,
    stdout=open(r"D:\vs code\sait\backend\out.log", "w"),
    stderr=subprocess.STDOUT,
)
print(f"Backend started PID {proc.pid}")
time.sleep(4)

try:
    r = urllib.request.urlopen("http://localhost:8000/api/matches/live", timeout=5)
    print("BACKEND OK", r.status, r.read()[:100])
except Exception as e:
    print("BACKEND ERROR:", e)
