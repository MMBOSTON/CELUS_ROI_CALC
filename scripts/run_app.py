import os
import sys

# Get the directory where the executable or script is located
base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
app_path = os.path.join(base_dir, 'roi_calculator_app.py')
os.system(f'streamlit run "{app_path}"')

# Update all file paths to use 'Template/ROI Calculator_v1.xlsx' or similar, instead of just the filename.
template_path = os.path.join(base_dir, 'Template', 'ROI Calculator_v1.xlsx')