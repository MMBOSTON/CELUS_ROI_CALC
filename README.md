# CELUS ROI Calculator

The **CELUS ROI Calculator** is a professional Streamlit web application that helps component manufacturers and suppliers estimate the financial impact of using the CELUS AI-based PCB design platform. By simulating different PCB production (BOM) scenarios, users can see how CELUS can increase lead generation, improve conversion rates, and boost indirect sales revenue.

## Features
- **Scenario-based ROI modeling**: Model multiple scenarios for different product/volume types.
- **Interactive UI**: Adjust assumptions and instantly see calculated results.
- **Scenario management**: Add, remove, duplicate, rename, save, load, and import/export scenarios.
- **Comparison tools**: Compare scenarios in table and chart form.
- **Export**: Download results as CSV, Excel, or PDF.
- **Compact, professional UI**: Modern, responsive, and highly compact layout.

## How It Works
- The app uses monthly estimates for BOM values and revenues.
- Users select or create scenarios, adjust assumptions (conversion rates, BOM value, etc.), and see the impact of CELUS adoption on revenue and conversion.
- Results are shown side-by-side for each scenario, with comparison tools for multiple scenarios.

## Quick Start

### 1. Clone the Repository
```bash
# Replace <repo-url> with the actual repository URL
git clone <repo-url>
cd CELUS_ROI_Calc
```

### 2. Set Up Python Environment
It is recommended to use a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run scripts/roi_calculator_app.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501).

## Packaging as a Standalone EXE (Windows)
A build script is provided for PyInstaller one-file builds:
```bash
# From the project root:
cd scripts
build.bat
```
The standalone EXE will be created in the `build/launch_app/` directory.

## File Structure
- `scripts/roi_calculator_app.py` — Main Streamlit app
- `requirements.txt` — Python dependencies
- `scenarios.json` — Saved scenarios (auto-generated)
- `Template/ROI Calculator_v1.xlsx` — Excel template for import/export
- `build.bat` — Build script for Windows EXE

## Notes
- The app is designed for Windows but can run on Mac/Linux with Python and Streamlit.
- All scenario and template files are saved locally.
- For best results, use the latest version of Chrome or Edge.

## Support
For questions or issues, please open an issue in the repository or contact the CELUS team.
