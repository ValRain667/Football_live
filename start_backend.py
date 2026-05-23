import subprocess
import time
import sys

backend_dir = "D:/vs code/sait/backend"
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=backend_dir,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
print(f"Backend started with PID {proc.pid}")
time.sleep(4)

import urllib.request
try:
    r = urllib.request.urlopen("http://localhost:8000/api/matches/live", timeout=5)
    print("BACKEND OK", r.status)
except Exception as e:
    print("BACKEND ERROR:", e)
