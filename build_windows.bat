@echo off
echo ===========================================
echo Building MOV2MP4 for Windows (x64)
echo ===========================================

:: Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist build_assets rmdir /s /q build_assets

mkdir build_assets\bin

:: Download FFmpeg (Windows x64) from BtbN
echo Downloading FFmpeg from BtbN...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'"
powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'build_assets\bin_temp'"
move build_assets\bin_temp\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe build_assets\bin\
rmdir /s /q build_assets\bin_temp
del ffmpeg.zip

echo Bundled FFmpeg version:
build_assets\bin\ffmpeg.exe -version

:: Install dependencies
pip install pyinstaller

:: Build the application (onedir)
echo Running PyInstaller...
pyinstaller --noconfirm ^
    --name "MOV2MP4" ^
    --onedir ^
    --windowed ^
    --add-binary "build_assets\bin\ffmpeg.exe;bin" ^
    --collect-data tkinterdnd2 ^
    gui.py

echo Build complete: dist\MOV2MP4

:: Note: User needs Inno Setup installed to run the final compiler.
:: A sample installer script (MOV2MP4.iss) should be compiled with:
:: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" MOV2MP4.iss

echo ===========================================
echo To create the installer, run Inno Setup on MOV2MP4.iss
echo ===========================================
