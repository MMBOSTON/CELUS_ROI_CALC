# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['scripts\\roi_calculator_app.py'],
    pathex=[],
    binaries=[],
    datas=[('..\\scenarios.json', '.'), ('..\\Template\\ROI Calculator_v1.xlsx', 'Template'), ('..\\sample_scenarios_template.csv', '.'), ('..\\celus_sq.jpg', '.')],
    hiddenimports=['xlsxwriter'],
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
    name='CELUS_ROI_Calc',
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
