#!/usr/bin/env python
# encoding: utf-8
"""
IceSettings.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

Basic settings to be used by the app.
"""

import sys
import os

appname = "Ice"
appdescription = "ROM Manager for Steam"
appauthor = "Scott Rice"

# The emulator paths listed below should all be relative to the 
# ice/resources/emulators/{platform} directory.
#
# For example, if the full path for Project 64 (Windows N64 emulator) was
# ice/resources/emulators/Windows/project64/pj64.exe
# Then windows_emulators["N64"] should be set as "project64/pj64.exe"

windows_emulators = {
    # "NES":          "",
    # "SNES":         "",
    # "N64":          "",
    # "Gamecube":     "",
    # "Wii":          "",
    # "PS1":          "",
    # "PS2":          "",
    # "Genesis":      "",
    # "Dreamcast":    "",
    # "Gameboy":      "",
    # "GBA":          "",
    # "DS":           "",
}

osx_emulators = {
    "NES":          "mednafen/mednafen",
    "SNES":         "Snes9x/Snes9x.app",
    "N64":          "mupen64plus/ice_run.sh",
    # "Gamecube":     "",
    # "Wii":          "",
    # "PS1":          "",
    # "PS2":          "",
    "Genesis":      "mednafen/mednafen",
    # "Dreamcast":    "",
    "Gameboy":      "mednafen/mednafen",
    "GBA":          "mednafen/mednafen",
    # "DS":           "",
}

linux_emulators = {
    # "NES":          "",
    # "SNES":         "",
    # "N64":          "",
    # "Gamecube":     "",
    # "Wii":          "",
    # "PS1":          "",
    # "PS2":          "",
    # "Genesis":      "",
    # "Dreamcast":    "",
    # "Gameboy":      "",
    # "GBA":          "",
    # "DS":           "",
}

emulator_paths = {
    "Windows":  windows_emulators,
    "OSX":      osx_emulators,
    "Linux":    linux_emulators
}

def platform_string():
    if sys.platform.startswith('win'):
        return "Windows"
    elif sys.platform.startswith('darwin'):
        return "OSX"
    else:
        return "Linux"
        
def emulator_exists(platform,console):
    return relative_emulator_path(platform,console) is not None
        
def relative_emulator_path(platform,console):
    try:
        return emulator_paths[platform][console.shortname]
    except KeyError:
        return None