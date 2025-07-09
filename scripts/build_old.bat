@echo off
REM --- Build and Package CELUS ROI Calculator Standalone App ---

REM Clean previous build artifacts
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
if exist scripts\__pycache__ rmdir /s /q scripts\__pycache__
if exist app_core\__pycache__ rmdir /s /q app_core\__pycache__

REM Build the executable with PyInstaller
REM --hidden-import=xlsxwriter is required for Excel export
REM --add-data includes required data files (use ; as separator on Windows)
pyinstaller --onefile --noconfirm --clean --name "CELUS_ROI_Calc" --add-data "..\scenarios.json;." --add-data "..\Template\ROI Calculator_v1.xlsx;Template" --add-data "..\sample_scenarios_template.csv;." --add-data "..\celus_sq.jpg;." --hidden-import=xlsxwriter scripts\roi_calculator_app.py

REM Create a README.txt for the package
set README_FILE=dist\README.txt
echo CELUS ROI Calculator Standalone App > %README_FILE%
echo. >> %README_FILE%
echo To run: >> %README_FILE%
echo 1. Unzip this package anywhere on your Windows PC. >> %README_FILE%
echo 2. Double-click CELUS_ROI_Calc.exe to launch the ROI Calculator. >> %README_FILE%
echo 3. No Python installation is required. >> %README_FILE%
echo. >> %README_FILE%
echo If you encounter missing data errors, ensure all files are extracted and in the same folder as the .exe. >> %README_FILE%
echo. >> %README_FILE%
echo For help, see the full documentation or contact support. >> %README_FILE%

REM Copy required files to dist folder (if not already copied by PyInstaller)
copy /Y ..\scenarios.json dist\ >nul 2>&1
if not exist dist\Template mkdir dist\Template
copy /Y ..\Template\ROI Calculator_v1.xlsx dist\Template\ >nul 2>&1
copy /Y ..\sample_scenarios_template.csv dist\ >nul 2>&1
copy /Y ..\celus_sq.jpg dist\ >nul 2>&1

REM Create a distributable ZIP package
cd dist
powershell -Command "Compress-Archive -Path CELUS_ROI_Calc.exe,scenarios.json,Template\'ROI Calculator_v1.xlsx',sample_scenarios_template.csv,celus_sq.jpg,README.txt -DestinationPath CELUS_ROI_Calc_Package.zip"
cd ..

echo Build and packaging complete. Distributable ZIP is at dist\CELUS_ROI_Calc_Package.zip
