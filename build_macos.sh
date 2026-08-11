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

# Install PyInstaller
pip install pyinstaller

# Build the application
echo "Running PyInstaller..."
pyinstaller --noconfirm \
    --name "MOV2MP4" \
    --onedir \
    --windowed \
    --add-binary "build_assets/bin/ffmpeg:bin" \
    --collect-data tkinterdnd2 \
    gui.py

echo "Build complete: dist/MOV2MP4.app"

# Verify execution structure
if [ -d "dist/MOV2MP4.app" ]; then
    echo "Creating DMG..."
    # We create the DMG inside dist/
    cd dist
    
    # If create-dmg fails (sometimes it complains about disk images), we fall back to hdiutil
    create-dmg \
      --volname "MOV2MP4 Installer" \
      --window-pos 200 120 \
      --window-size 600 400 \
      --icon-size 100 \
      --icon "MOV2MP4.app" 175 120 \
      --hide-extension "MOV2MP4.app" \
      --app-drop-link 425 120 \
      "MOV2MP4.dmg" \
      "MOV2MP4.app" || {
          echo "create-dmg failed, falling back to hdiutil..."
          hdiutil create -volname "MOV2MP4" -srcfolder MOV2MP4.app -ov -format UDZO MOV2MP4.dmg
      }
      
    echo "Packaging complete: dist/MOV2MP4.dmg"
else
    echo "Error: MOV2MP4.app was not found in dist/"
    exit 1
fi
