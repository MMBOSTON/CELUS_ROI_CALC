@echo off
REM Batch file to package the standalone ROI Calculator app for sharing

REM Set variables
set DIST_DIR=%~dp0dist
set SHARE_DIR=%~dp0share_test

REM Remove old share_test folder if it exists
if exist "%SHARE_DIR%" rmdir /s /q "%SHARE_DIR%"

REM Create new share_test folder
mkdir "%SHARE_DIR%"

REM Copy the executable
copy "%DIST_DIR%\launch_app.exe" "%SHARE_DIR%\"

REM Copy scenarios.json and sample_scenarios_template.csv
copy "%~dp0scenarios.json" "%SHARE_DIR%\"
copy "%~dp0sample_scenarios_template.csv" "%SHARE_DIR%\"

REM Copy Template folder and its contents (case-insensitive fix)
xcopy "%~dp0Template" "%SHARE_DIR%\Template" /E /I /Y

REM Copy README.txt if it exists
if exist "%~dp0share\README.txt" copy "%~dp0share\README.txt" "%SHARE_DIR%\"

REM Copy icon if it exists
if exist "%~dp0celus_sq.ico" copy "%~dp0celus_sq.ico" "%SHARE_DIR%\"

@echo Packaging complete. Files are in %SHARE_DIR%
pause
