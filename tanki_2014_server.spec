# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports=[
        'bitstring',
        'bitstring.bitstore',
        'bitstring.bitstore_bitarray',
        'bitstring.bitstore_bitarray_helpers',
        'bitstring.bitstore_common_helpers'
    ]
hiddenimports += collect_submodules("mysql.connector")
hiddenimports += collect_submodules("mysql")

datas = []
datas += collect_data_files("mysql.connector")
datas += collect_data_files("mysql")

a = Analysis(
    ['scripts\\tanki_2014_server.py'],
    pathex=[],
    binaries=[],
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
    a.binaries,
    a.datas,
    [],
    name='tanki_2014_server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
