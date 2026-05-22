import subprocess
import sys
import os
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(ROOT, "backend")
FRONTEND_DIR = os.path.join(ROOT, "frontend")


def is_port_open(port):
    try:
        urllib.request.urlopen(f"http://localhost:{port}", timeout=2)
        return True
    except Exception:
        return False


def kill_port_process(port):
    """Kill process listening on a given port (Windows)."""
    try:
        result = subprocess.run(
            ["netstat", "-ano", "-p", "tcp"],
            capture_output=True, text=True, check=False
        )
        for line in result.stdout.splitlines():
            if f":{port}" in line and "LISTENING" in line:
                parts = line.strip().split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    subprocess.run(["taskkill", "/f", "/pid", pid], capture_output=True, check=False)
                    return True
    except Exception:
        pass
    return False


def main():
    # 1. Check / free ports
    for port in [8000, 3000]:
        if is_port_open(port):
            print(f"Port {port} is busy. Stopping old process...")
            kill_port_process(port)
            time.sleep(2)

    # 2. Setup environment
    env = os.environ.copy()
    env["PYTHONPATH"] = BACKEND_DIR
    env["PATH"] = r"C:\Program Files;" + env.get("PATH", "")

    backend_proc = None
    frontend_proc = None

    try:
        # 3. Start backend
        print("Starting backend on http://localhost:8000 ...")
        backend_proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd=BACKEND_DIR,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        time.sleep(4)

        # 4. Start frontend
        print("Starting frontend on http://localhost:3000 ...")
        frontend_proc = subprocess.Popen(
            [r"C:\Program Files\npm.cmd", "run", "dev"],
            cwd=FRONTEND_DIR,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        time.sleep(6)

        # 5. Health checks
        backend_ok = is_port_open(8000)
        frontend_ok = is_port_open(3000)

        if backend_ok and frontend_ok:
            print("\n" + "=" * 50)
            print("All services are running!")
            print("  Backend : http://localhost:8000")
            print("  Frontend: http://localhost:3000")
            print("=" * 50)
            print("Press Ctrl+C to stop.\n")
        else:
            if not backend_ok:
                print("WARNING: Backend did not respond on port 8000")
            if not frontend_ok:
                print("WARNING: Frontend did not respond on port 3000")
            print("\nPress Ctrl+C to stop.\n")

        # 6. Keep running + stream logs
        while True:
            # Stream backend output
            if backend_proc.poll() is None:
                try:
                    line = backend_proc.stdout.readline()
                    if line:
                        print(f"[BACKEND] {line.rstrip()}")
                except Exception:
                    pass

            # Stream frontend output
            if frontend_proc.poll() is None:
                try:
                    line = frontend_proc.stdout.readline()
                    if line:
                        print(f"[FRONTEND] {line.rstrip()}")
                except Exception:
                    pass

            # Check if both died
            if backend_proc.poll() is not None and frontend_proc.poll() is not None:
                print("Both processes exited.")
                break

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        if backend_proc and backend_proc.poll() is None:
            backend_proc.terminate()
            try:
                backend_proc.wait(timeout=3)
            except Exception:
                backend_proc.kill()
        if frontend_proc and frontend_proc.poll() is None:
            frontend_proc.terminate()
            try:
                frontend_proc.wait(timeout=3)
            except Exception:
                frontend_proc.kill()
        print("Done.")


if __name__ == "__main__":
    main()
