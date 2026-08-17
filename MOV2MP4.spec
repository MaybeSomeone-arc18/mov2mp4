# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files

is_win = sys.platform.startswith('win')

datas = []
hiddenimports = []

for pkg in ['customtkinter', 'tkinterdnd2', 'PIL', 'tqdm', 'darkdetect']:
    try:
        datas += collect_data_files(pkg)
        hiddenimports += collect_submodules(pkg)
    except Exception:
        pass

if os.path.exists('assets'):
    datas.append(('assets', 'assets'))

if is_win:
    ffmpeg_binary = ('build_assets/bin/ffmpeg.exe', 'bin')
    icon_path = 'assets/icon.ico'
else:
    ffmpeg_binary = ('build_assets/bin/ffmpeg', 'bin')
    icon_path = 'assets/icon.icns'

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[ffmpeg_binary],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MOV2MP4',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MOV2MP4',
)

if not is_win:
    app = BUNDLE(
        coll,
        name='MOV2MP4.app',
        icon=icon_path,
        bundle_identifier=None,
    )
