# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['reactautomationtoolv3.pyw'],
    pathex=['.'],
    binaries=[
    ('C:\\hostedtoolcache\\windows\\Python\\3.8.10\\x64\\python38.dll', '.'),
    ],
    datas=[
        ('app_icon.py', '.'),
        ('app_icons.py', '.'),
        ('icons/*', 'icons')
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
    [],
    name='reactautomationtoolv3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='react.ico'
    onefile=True
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
