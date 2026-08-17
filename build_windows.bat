@echo off
setlocal enabledelayedexpansion
echo ===========================================
echo Building MOV2MP4 for Windows (x64)
echo ===========================================

:: 1. Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist build_assets rmdir /s /q build_assets

:: 2. Prepare build_assets
mkdir build_assets\bin

:: 3. Download ONLY the pinned BtbN FFmpeg build
set "FFMPEG_URL=https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2026-08-10-13-17/ffmpeg-N-126039-g6bbc22dc09-win64-gpl.zip"

echo Downloading pinned FFmpeg build from BtbN...
echo URL: !FFMPEG_URL!

powershell -Command "$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri '!FFMPEG_URL!' -OutFile 'ffmpeg.zip'"
if errorlevel 1 (
    echo [ERROR] Failed to download pinned FFmpeg release from BtbN.
    echo Please verify network connectivity or check if URL is available.
    exit /b 1
)

if not exist ffmpeg.zip (
    echo [ERROR] ffmpeg.zip was not created during download.
    exit /b 1
)

:: 4. Extract ffmpeg.exe
echo Extracting FFmpeg archive...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'build_assets\bin_temp'"
if errorlevel 1 (
    echo [ERROR] Failed to extract ffmpeg.zip.
    exit /b 1
)

move build_assets\bin_temp\ffmpeg-N-126039-g6bbc22dc09-win64-gpl\bin\ffmpeg.exe build_assets\bin\ >nul
rmdir /s /q build_assets\bin_temp
del ffmpeg.zip

if not exist build_assets\bin\ffmpeg.exe (
    echo [ERROR] ffmpeg.exe not found in build_assets\bin\ after extraction.
    exit /b 1
)

:: 5. Verify ffmpeg.exe works
echo Verifying downloaded FFmpeg binary...
build_assets\bin\ffmpeg.exe -version | findstr /C:"ffmpeg version"
if errorlevel 1 (
    echo [ERROR] ffmpeg.exe execution verification failed.
    exit /b 1
)

:: Install PyInstaller and requirements if not present
py -m pip install pyinstaller
py -m pip install -r requirements.txt

:: 6 & 7. Build ONEDIR application using MOV2MP4.spec (includes assets\icon.ico)
echo Running PyInstaller with MOV2MP4.spec...
py -m PyInstaller --noconfirm MOV2MP4.spec
if errorlevel 1 (
    echo [ERROR] PyInstaller build failed.
    exit /b 1
)


:: 8. Verify resulting MOV2MP4.exe exists
if not exist dist\MOV2MP4\MOV2MP4.exe (
    echo [ERROR] Build verification failed: dist\MOV2MP4\MOV2MP4.exe does not exist.
    exit /b 1
)

:: 9. Verify bundled bin\ffmpeg.exe exists
set "FFMPEG_BUNDLED="
if exist dist\MOV2MP4\_internal\bin\ffmpeg.exe set "FFMPEG_BUNDLED=dist\MOV2MP4\_internal\bin\ffmpeg.exe"
if exist dist\MOV2MP4\bin\ffmpeg.exe set "FFMPEG_BUNDLED=dist\MOV2MP4\bin\ffmpeg.exe"

if "!FFMPEG_BUNDLED!"=="" (
    echo [ERROR] Build verification failed: bundled ffmpeg.exe was not found inside dist\MOV2MP4.
    exit /b 1
)

echo ===========================================
echo [SUCCESS] PyInstaller ONEDIR bundle created at dist\MOV2MP4
echo [SUCCESS] Bundled binary verified at !FFMPEG_BUNDLED!
echo ===========================================

:: 10. Search for Inno Setup Compiler (ISCC.exe) and compile
set "ISCC_PATH="
if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" set "ISCC_PATH=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set "ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set "ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"

if "!ISCC_PATH!"=="" (
    where iscc >nul 2>&1
    if not errorlevel 1 set "ISCC_PATH=iscc"
)

if not "!ISCC_PATH!"=="" (
    echo Compiling Windows Installer with Inno Setup...
    echo Compiler path: !ISCC_PATH!
    "!ISCC_PATH!" MOV2MP4.iss
    if errorlevel 1 (
        echo [ERROR] Inno Setup compilation failed.
        exit /b 1
    )
    if exist dist\MOV2MP4-Setup.exe (
        echo ===========================================
        echo [SUCCESS] Windows Installer created: dist\MOV2MP4-Setup.exe
        echo ===========================================
    ) else (
        echo [ERROR] Installer creation failed: dist\MOV2MP4-Setup.exe missing.
        exit /b 1
    )
) else (
    echo ===========================================
    echo [ERROR] Inno Setup Compiler ISCC.exe was not found.
    echo PyInstaller ONEDIR build is complete at: dist\MOV2MP4
    echo ===========================================
    exit /b 1
)
