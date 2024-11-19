# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['arduino_logique.py',
    'breadboard.py',
    'component_params.py',
    'component_sketch.py',
    'dataCDLT.py',
    'menus.py',
    'sidebar.py',
    'toolbar.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Assets', 'Assets'),
        ('Components', 'Components'),
        ('Components', 'Components'),
        ('object_model', 'object_model'),
        ('Images', 'Images'),
        ('__pycache__', '__pycache__'),
        ('pyserial-3.5.dist-info', 'pyserial')
    ],
    hiddenimports=[
        'serial',
    ],
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
    name='arduino_logique',
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

coll = COLLECT(
     exe, 
     a.binaries, 
     a.zipfiles, 
     a.datas, 
     strip=False, 
     upx=True, 
     upx_exclude=[], 
     name='arduino_logique',
     debug=True,
     target_arch=None,
     codesign_identity=None,
     entitlements_file=None,
     xarc={'format': 'zip', 'file': 'arduino_logique.zip'}
)