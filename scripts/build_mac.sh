#!/bin/bash
# build_mac.sh
# Build the CELUS ROI Calculator as a standalone macOS executable using PyInstaller
# Run this script on a Mac with Python and PyInstaller installed

set -e

# Clean previous build artifacts
rm -rf build dist launch_app.spec

# Ensure roi_calculator_app.py exists
if [ ! -f roi_calculator_app.py ]; then
  echo "ERROR: roi_calculator_app.py not found!"
  exit 1
fi

# Set icon if available (macOS .icns format is required for --icon)
ICON="celus_sq.icns"
ICON_ARG=""
if [ -f "$ICON" ]; then
  ICON_ARG="--icon=$ICON"
fi

# Build the app
pyinstaller --noconfirm --onefile $ICON_ARG \
  --add-data "Template:Template" \
  --add-data "ROI Calculator_v1.xlsx:." \
  --add-data "roi_calculator_app.py:." \
  launch_app.py

# Output
if [ -f dist/launch_app ]; then
  echo "Build complete! The standalone executable is in the 'dist' folder."
else
  echo "Build failed."
fi
