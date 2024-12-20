# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['reactautomationtoolv3.pyw'],  # Your main script
    pathex=[],
    binaries=[],
    datas=[
        ('app_icon.py', '.'),        # Include app_icon.py
        ('app_icons.py', '.'),       # Include app_icons.py
        ('icons/*', 'icons')         # Include all files in the icons directory
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='reactautomationtoolv3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='react.ico'  # Specify the correct path to your icon file here
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='reactautomationtoolv3'
)
