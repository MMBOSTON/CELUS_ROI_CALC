@echo off
REM Build the Streamlit ROI Calculator as a single-file Windows executable
REM Requires: pyinstaller, celus_sq.ico (optional), and all data files in place

REM Ensure roi_calculator_app.py exists
if not exist "scripts\roi_calculator_app.py" (
    echo ERROR: roi_calculator_app.py not found!
    exit /b 1
)

REM Clean previous build artifacts
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist launch_app.spec del /q launch_app.spec

REM Set icon variable to celus_sq.ico if it exists, otherwise leave blank
set ICON=celus_sq.ico
if not exist "%ICON%" set ICON=

REM Build command with or without icon
if not "%ICON%"=="" (
        pyinstaller --noconfirm --onefile --icon=%ICON% --add-data "Template;Template" --add-data "Template\ROI Calculator_v1.xlsx;Template" --add-data "scripts\roi_calculator_app.py;." scripts\launch_app.py
) else (
        pyinstaller --noconfirm --onefile --add-data "Template;Template" --add-data "Template\ROI Calculator_v1.xlsx;Template" --add-data "scripts\roi_calculator_app.py;." scripts\launch_app.py
)

echo Build complete. Press any key to exit.
pause
