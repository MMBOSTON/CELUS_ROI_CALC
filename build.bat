@echo off
echo === build.bat started ===

REM Build script for CELUS ROI Calculator Standalone Windows App

REM Redirect all output to build.log and also show in terminal
set LOGFILE=build.log
REM Clear previous log
if exist %LOGFILE% del %LOGFILE%

REM Always work from the project root (where this script is located)
setlocal
set "ROOT=%~dp0"
cd /d "%ROOT%"

REM Debug: print current directory
echo Current directory: %CD%

REM Clean previous build artifacts
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist package rmdir /s /q package
if exist scripts\__pycache__ rmdir /s /q scripts\__pycache__
if exist scripts\*.spec del /q scripts\*.spec

REM Activate virtual environment (if not already active)
if not exist CELUS_ROI_Calc\Scripts\activate.bat (
    echo ERROR: Virtual environment activation script not found! Exiting.
    exit /b 1
)
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call CELUS_ROI_Calc\Scripts\activate.bat
    echo Virtual environment activated.
)

REM Build the executable with PyInstaller (run from project root)
powershell -Command "pyinstaller --noconfirm --hidden-import=xlsxwriter --add-data \"data\\scenarios.json;data\" --add-data \"celus_sq.jpg;.\" --add-data \"Template\\ROI Calculator_v1.xlsx;Template\" --add-data \"data\\sample_scenarios_template.csv;data\" --collect-all streamlit --collect-submodules streamlit --collect-data streamlit --collect-data importlib_metadata launcher.py --name CELUS_ROI_Calculator 2>&1 | Tee-Object -FilePath build.log -Append"

REM Check if the .exe was created
if not exist dist\CELUS_ROI_Calculator.exe (
    echo ERROR: PyInstaller build failed. Executable not found. Aborting packaging. See build.log for details.>> build.log
    echo ERROR: PyInstaller build failed. Executable not found. Aborting packaging. See build.log for details.
    exit /b 1
)

REM Create package directory
mkdir package

REM Copy the .exe
REM Copy the folder instead of just the .exe
xcopy /E /I /Y dist\CELUS_ROI_Calculator package\ >> build.log 2>&1
if errorlevel 1 echo ERROR: Failed to copy dist\CELUS_ROI_Calculator to package\>> build.log

REM Copy required data files
if not exist package\data mkdir package\data
copy data\scenarios.json package\data\ >> build.log 2>&1
if errorlevel 1 echo ERROR: Failed to copy data\scenarios.json>> build.log
copy celus_sq.jpg package\ >> build.log 2>&1
if errorlevel 1 echo ERROR: Failed to copy celus_sq.jpg>> build.log
if not exist package\Template mkdir package\Template

REM Debug: List contents of Template directory before copy
if exist Template dir Template >> build.log 2>&1

REM Check if the file exists before copying
if exist "Template\ROI Calculator_v1.xlsx" (
    echo File found: Template\ROI Calculator_v1.xlsx >> build.log
) else (
    echo ERROR: File NOT FOUND: Template\ROI Calculator_v1.xlsx >> build.log
)

copy "Template\ROI Calculator_v1.xlsx" package\Template\ >> build.log 2>&1
if errorlevel 1 echo ERROR: Failed to copy Template\ROI Calculator_v1.xlsx>> build.log
if exist data\sample_scenarios_template.csv copy data\sample_scenarios_template.csv package\data\ >> build.log 2>&1

REM Add README.txt for end users
(
echo CELUS ROI Calculator - Standalone Windows App
echo =============================
echo 1. Double-click CELUS_ROI_Calculator.exe to launch the app.
echo 2. The app will open in your default web browser.
echo 3. All required data files are included in this folder.
echo 4. No installation or Python required.
echo.
echo If you encounter issues, ensure all files are in the same folder as the .exe.
echo For support, contact: support@celus.io
) > package\README.txt

REM Zip the package for distribution
powershell -Command "Compress-Archive -Path package\* -DestinationPath CELUS_ROI_Calculator_Windows.zip -Force"
echo Zipped package to CELUS_ROI_Calculator_Windows.zip >> build.log

echo Build and packaging complete. Distributable ZIP: CELUS_ROI_Calculator_Windows.zip
echo Build and packaging complete. See build.log for details.