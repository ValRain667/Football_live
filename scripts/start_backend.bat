@echo off
chcp 65001 >nul
set PYTHONPATH=%~dp0..\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
