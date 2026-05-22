import urllib.request
import sys

try:
    r = urllib.request.urlopen("http://localhost:8000/api/matches/live", timeout=5)
    print("BACKEND OK", r.status)
except Exception as e:
    print("BACKEND ERROR:", e)

try:
    r = urllib.request.urlopen("http://localhost:3000", timeout=5)
    print("FRONTEND OK", r.status)
except Exception as e:
    print("FRONTEND ERROR:", e)
