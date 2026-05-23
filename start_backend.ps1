$bp = "$PSScriptRoot\backend"
$env:PYTHONPATH = $bp
Start-Process python -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8000" -WorkingDirectory $bp -RedirectStandardOutput "$bp\out.txt" -RedirectStandardError "$bp\err.txt"
Start-Sleep -Seconds 4
Get-Content "$bp\out.txt" | Select-Object -First 10
Get-Content "$bp\err.txt" | Select-Object -First 10
python -c "import urllib.request; r=urllib.request.urlopen('http://localhost:8000/api/matches/live', timeout=5); print('BACKEND OK', r.status)"
