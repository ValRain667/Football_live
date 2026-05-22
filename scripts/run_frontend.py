import subprocess
import os

env = os.environ.copy()
env["PATH"] = r"C:\Program Files;" + env.get("PATH", "")

proc = subprocess.Popen(
    [r"C:\Program Files\npm.cmd", "run", "dev"],
    cwd=r"D:\vs code\sait\frontend",
    env=env,
    stdout=open(r"D:\vs code\sait\frontend\out.log", "w"),
    stderr=subprocess.STDOUT,
)
print(f"Frontend started with PID {proc.pid}")
