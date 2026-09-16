@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0scripts"
py -3 export_ai_conversations.py 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Export script failed with exit code %errorlevel%
    exit /b %errorlevel%
)
