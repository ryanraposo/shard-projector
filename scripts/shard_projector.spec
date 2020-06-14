# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['..\\source\\model.py'],
             pathex=['C:\\Users\\ryanr\\source\\shard-projector\\scripts'],
             binaries=[],
             datas=[('../img/*', './icon'), ('../img/*', './img'), ('../data/ini/cluster_configuration.json', './data/ini'), ('../data/ini/shard_configuration.json', './data/ini')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='shard_projector',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='..\\img\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='shard_projector')
