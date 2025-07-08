# build_roi_app.ps1
# PowerShell script to package CELUS ROI Calculator as a standalone Windows executable

Write-Host "Cleaning previous build artifacts..."
Remove-Item -Recurse -Force build, dist, *.spec, __pycache__ -ErrorAction SilentlyContinue

# Optional: Create a custom PyInstaller hook for fpdf2 (improves reliability)
$hookContent = @"
from PyInstaller.utils.hooks import collect_submodules
hiddenimports = collect_submodules('fpdf')
"@
Set-Content -Path ".\hook-fpdf.py" -Value $hookContent -Encoding UTF8

Write-Host "Building the executable with PyInstaller..."
pyinstaller `
  --onefile `
  --add-data "templates;templates" `
  --add-data "scenarios.json;." `
  --add-data "sample_scenarios_template.csv;." `
  --add-data "pyinstaller-venv\Lib\site-packages\streamlit-1.46.1.dist-info;streamlit-1.46.1.dist-info" `
  --hidden-import=fpdf `
  --hidden-import=fpdf.html `
  --hidden-import=fpdf.fonts `
  --hidden-import=fpdf.enums `
  --hidden-import=fpdf.errors `
  --hidden-import=fpdf.glyphlist `
  --hidden-import=fpdf.syntax `
  --hidden-import=fpdf.template `
  --hidden-import=fpdf.translations `
  --hidden-import=fpdf.util `
  --additional-hooks-dir=. `
  launch_app.py

Write-Host ""
Write-Host "Build complete. The standalone .exe is in the 'dist' folder."
Write-Host "Test the .exe by double-clicking it in Windows Explorer."
Write-Host ""
Write-Host "If you still see 'ModuleNotFoundError: No module named ''fpdf''', please report the full error message."