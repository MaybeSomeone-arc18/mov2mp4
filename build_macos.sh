#!/bin/bash
set -e

echo "==========================================="
echo "Building MOV2MP4 for macOS (Apple Silicon)"
echo "==========================================="

# Clean previous builds
rm -rf build dist build_assets
mkdir -p build_assets/bin

# Download FFmpeg (macOS native arm64)
echo "Downloading FFmpeg from OSXExperts..."
curl -L -s "https://www.osxexperts.net/ffmpeg9arm.zip" -o ffmpeg.zip
unzip -q ffmpeg.zip -d build_assets/bin/
chmod +x build_assets/bin/ffmpeg
rm ffmpeg.zip

echo "==========================================="
echo "FFmpeg Binary Verification"
echo "==========================================="
file build_assets/bin/ffmpeg
echo ""
echo "Version Info:"
build_assets/bin/ffmpeg -version | head -n 3
echo ""
echo "License Configuration:"
build_assets/bin/ffmpeg -L | grep -i "GPL" || echo "GPL string not found in -L"
echo "==========================================="

# Use PyInstaller from .venv if available to avoid system environment package conflicts
PYINSTALLER_BIN="pyinstaller"
if [ -f ".venv/bin/pyinstaller" ]; then
    PYINSTALLER_BIN=".venv/bin/pyinstaller"
else
    pip install pyinstaller
fi

# Build the application
echo "Running PyInstaller..."
"$PYINSTALLER_BIN" --noconfirm \
    --name "MOV2MP4" \
    --onedir \
    --windowed \
    --icon "assets/icon.icns" \
    --add-binary "build_assets/bin/ffmpeg:bin" \
    --collect-data tkinterdnd2 \
    gui.py

echo "Build complete: dist/MOV2MP4.app"

# Verify execution structure
if [ -d "dist/MOV2MP4.app" ]; then
    echo "Preparing DMG staging folder..."
    rm -rf dist/dmg_stage
    mkdir -p dist/dmg_stage
    cp -R dist/MOV2MP4.app dist/dmg_stage/
    cp "Launch MOV2MP4.command" dist/dmg_stage/
    chmod +x "dist/dmg_stage/Launch MOV2MP4.command"
    ln -s /Applications dist/dmg_stage/Applications

    cd dist
    echo "Creating DMG..."
    create-dmg \
      --volname "MOV2MP4 Installer" \
      --window-pos 200 120 \
      --window-size 600 400 \
      --icon-size 100 \
      --icon "MOV2MP4.app" 140 120 \
      --app-drop-link 300 120 \
      --icon "Launch MOV2MP4.command" 460 120 \
      --hide-extension "MOV2MP4.app" \
      "MOV2MP4.dmg" \
      "dmg_stage" || {
          echo "create-dmg failed, falling back to hdiutil..."
          hdiutil create -volname "MOV2MP4" -srcfolder dmg_stage -ov -format UDZO MOV2MP4.dmg
      }
      
    echo "Packaging complete: dist/MOV2MP4.dmg"
else
    echo "Error: MOV2MP4.app was not found in dist/"
    exit 1
fi
