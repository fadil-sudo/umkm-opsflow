@echo off
echo ==========================================
echo   UMKM OpsFlow - Streamlit UI Launcher
echo ==========================================
echo.

REM Use the managed Python venv with Streamlit installed
set PYTHON=C:\Users\User\.workbuddy-ai\binaries\python\envs\default\Scripts\python.exe

echo Checking Python...
"%PYTHON%" --version

echo.
echo Starting Streamlit UI...
echo Open browser at: http://localhost:8501
echo.

cd /d "C:\Users\User\WorkBuddy AI\2026-10-27-20-34-13\umkm-opsflow"
"%PYTHON%" -m streamlit run app.py

pause