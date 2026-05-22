import subprocess
import sys
import os

env = os.environ.copy()
env["PYTHONPATH"] = r"D:\vs code\sait\backend"
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=r"D:\vs code\sait\backend",
    env=env,
    stdout=open(r"D:\vs code\sait\backend\out.log", "w"),
    stderr=subprocess.STDOUT,
)
print(f"Backend started with PID {proc.pid}")
