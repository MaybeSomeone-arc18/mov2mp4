#!/bin/bash

APP_PATH="/Applications/MOV2MP4.app"
EXEC_PATH="/Applications/MOV2MP4.app/Contents/MacOS/MOV2MP4"

echo "==========================================="
echo "  MOV2MP4 Launcher"
echo "==========================================="
echo ""

if [ ! -d "$APP_PATH" ]; then
    echo "Could not find MOV2MP4 in your Applications folder."
    echo ""
    echo "Please drag MOV2MP4.app into Applications and try again."
    echo ""
    echo "Press any key to exit..."
    read -n 1 -s
    exit 1
fi

echo "Preparing MOV2MP4..."
xattr -dr com.apple.quarantine "$APP_PATH" 2>/dev/null || true

echo "Launching MOV2MP4..."
echo ""

if [ -f "$EXEC_PATH" ]; then
    "$EXEC_PATH" > /dev/null 2>&1 &
    exit 0
else
    echo "Could not find application executable inside MOV2MP4.app."
    echo ""
    echo "Please drag MOV2MP4.app into Applications again."
    echo ""
    echo "Press any key to exit..."
    read -n 1 -s
    exit 1
fi
