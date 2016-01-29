# -*- mode: python -*-

block_cipher = None

df = [
	'config.txt',
	'emulators.txt',
	'consoles.txt',
]

a = Analysis(['ice\\__main__.py'],
             pathex=['c:\\Users\\Scott\\Development\\Projects\\Ice\\ice'],
             binaries=None,
             datas=map(lambda f: (f, ''), df),
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Ice',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Ice')
