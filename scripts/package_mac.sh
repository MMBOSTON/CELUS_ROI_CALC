#!/bin/bash
# package_mac.sh
# Package and zip the standalone Mac app for distribution
# Run this after build_mac.sh

set -e

DIST_DIR="dist"
SHARE_DIR="share_mac"
ZIP_NAME="share_mac.zip"

# Clean previous share folder and zip
rm -rf "$SHARE_DIR" "$ZIP_NAME"

# Create share folder
mkdir "$SHARE_DIR"

# Copy the executable
cp "$DIST_DIR/launch_app" "$SHARE_DIR/"

# Copy required data files
cp scenarios.json "$SHARE_DIR/" 2>/dev/null || true
cp sample_scenarios_template.csv "$SHARE_DIR/" 2>/dev/null || true

# Copy Template folder
cp -R Template "$SHARE_DIR/" 2>/dev/null || true

# Copy README if exists
cp share/README.txt "$SHARE_DIR/" 2>/dev/null || true

# Copy icon if exists
cp celus_sq.icns "$SHARE_DIR/" 2>/dev/null || true

# Zip the share folder
zip -r "$ZIP_NAME" "$SHARE_DIR"

echo "Packaging complete. $ZIP_NAME is ready for distribution."
