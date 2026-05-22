@echo off
chcp 65001 >nul
echo Starting Football Live Hub...
start "Backend" cmd /k "%~dp0start_backend.bat"
timeout /t 3 >nul
start "Frontend" cmd /k "%~dp0start_frontend.bat"
echo Both services started.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
