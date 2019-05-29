import os

from steam import model


def test_read_single_shortcut():
    input_bytes = b'\x00\x01AppName\x00SURVEY_PROGRAM\x00\x01Exe\x00"C:\\Program Files (x86)\\SURVEY_PROGRAM\\DELTARUNE.exe"\x00\x01StartDir\x00"C:\\Program Files (x86)\\SURVEY_PROGRAM\\"\x00\x01icon\x00\x00\x01ShortcutPath\x00\x00\x01LaunchOptions\x00\x00\x02IsHidden\x00\x00\x00\x00\x00\x02AllowDesktopConfig\x00\x01\x00\x00\x00\x02AllowOverlay\x00\x01\x00\x00\x00\x02OpenVR\x00\x00\x00\x00\x00\x02Devkit\x00\x00\x00\x00\x00\x01DevkitGameID\x00\x00\x02LastPlayTime\x00???\x00tags\x00\x08\x08\x08\x08'
    shortcut = model.Shortcut.parse_from_bytes(input_bytes)

    assert shortcut.name == "SURVEY_PROGRAM"
    assert shortcut.exe == "C:\\Program Files (x86)\\SURVEY_PROGRAM\\DELTARUNE.exe"
    assert shortcut.startdir == "C:\\Program Files (x86)\\SURVEY_PROGRAM\\"


def test_read_shortcut_vdf_single():
    shortcuts_vdf_path = os.path.join(os.path.dirname(__file__), 'vdf', 'single.vdf')
    shortcuts = model.parse_shortcuts_vdf(shortcuts_vdf_path)
    assert len(shortcuts) == 1

    shortcut = shortcuts[0]
    assert shortcut.name == "SURVEY_PROGRAM"
    assert shortcut.exe == "C:\\Program Files (x86)\\SURVEY_PROGRAM\\DELTARUNE.exe"
    assert shortcut.startdir == "C:\\Program Files (x86)\\SURVEY_PROGRAM\\"


def test_read_shortcut_vdf_triple():
    shortcuts_vdf_path = os.path.join(os.path.dirname(__file__), 'vdf', 'triple.vdf')
    shortcuts = model.parse_shortcuts_vdf(shortcuts_vdf_path)
    assert len(shortcuts) == 3

    for shortcut in shortcuts:
        assert shortcut.name == 'Kingdom Hearts'
        assert shortcut.exe == 'C:\\Program Files (x86)\\Emulator Copies\\Kingdom Hearts\\pcsx2-r5350.exe C:\\Users\\Scott.Scott-PC\\ROMs\\PS2\\Kingdom Hearts.iso'
        assert shortcut.startdir == 'C:\\Program Files (x86)\\Emulator Copies\\Kingdom Hearts\\'

