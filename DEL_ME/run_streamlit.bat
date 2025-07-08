@echo off
REM Stop all Python processes (use with care!)
taskkill /F /IM python.exe >nul 2>&1
REM Wait a moment for processes to close
ping 127.0.0.1 -n 2 > nul
REM Start Streamlit app
cd /d %~dp0
call venv\Scripts\activate
call streamlit run roi_calculator_app.py
