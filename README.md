# CELUS ROI Calculator

This project is a web-based Return on Investment (ROI) Calculator for component manufacturers and suppliers using the CELUS AI-based PCB design platform. The calculator helps estimate the financial impact of CELUS on lead generation and indirect sales, based on user analytics and conversion improvements.

## Features
- Interactive web app built with Streamlit
- Multiple scenarios (Prototype, Medium Volume, High Volume) with customizable assumptions
- Collapsible sections for each scenario's inputs and results
- Sidebar for scenario selection
- Real-time calculation of key metrics, including:
  - Total Value per BOM
  - Converted Users
  - Total BOM Value from Users
  - Value to Production
  - Revenue from Indirect Sales
  - CELUS-specific conversion and revenue metrics
  - Multiplier and Annual Revenue with CELUS
- Can be run as a standalone desktop app (packaged with PyInstaller)

## How to Run (Development)
1. Clone the repository or download the project files.
2. (Optional) Create and activate a Python virtual environment.
3. Install dependencies:
   ```
   pip install streamlit
   ```
4. Start the app:
   ```
   streamlit run roi_calculator_app.py
   ```
5. The app will open in your browser at `http://localhost:8501`.

## How to Build a Standalone App (Windows)
1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Build the executable (from the project root):
   ```
   pyinstaller --onefile --add-data "roi_calculator_app.py;." run_app.py
   ```
3. The standalone app will be in the `dist` folder as `run_app.exe`.

## Project Structure
```
CELUS_ROI_Calc/
│
├── roi_calculator_app.py         # Main Streamlit app
├── run_app.py                    # Launcher script for standalone app
├── README.md                     # Project documentation
├── dist/                         # PyInstaller output (ignore for editing)
├── build/                        # PyInstaller build files (ignore)
├── venv/                         # Python virtual environment (ignore)
└── ...                           # Other files
```

## Version Control
To enable version control with Git:
1. Initialize a git repository:
   ```
   git init
   ```
2. Add all files:
   ```
   git add .
   ```
3. Commit:
   ```
   git commit -m "Initial commit: CELUS ROI Calculator app"
   ```
4. (Optional) Connect to a remote repository (e.g., GitHub) and push your code.

---

For questions or improvements, please contact the CELUS team.
