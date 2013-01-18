#!/usr/bin/env python
# encoding: utf-8
"""
IceEmulatorManager.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

from emulators import *

# List of emulators to use for each conole

windows_emulators = {
    "NES":          winbsnes.Winbsnes("NES"),
    "SNES":         winbsnes.Winbsnes("SNES"),
    "N64":          winproject64.WinProject64("N64"),
    "Gamecube":     windolphin.WinDolphin("Gamecube"),
    # "Wii":          windolphin.WinDolphin("Wii"),
    # "PS1":          ,
    # "PS2":          ,
    # "Genesis":      ,
    # "Dreamcast":    ,
    "Gameboy":      winbsnes.Winbsnes("Gameboy"),
    "GBA":          winvisualboyadvance.WinVisualBoyAdvance("GBA"),
}

osx_emulators = {
    "NES":          macmednafen.MacMednafen("NES"),
    "SNES":         macsnes9x.MacSnes9x("SNES"),
    # "N64":          ,
    # "Gamecube":     ,
    # "Wii":          ,
    # "PS1":          ,
    # "PS2":          ,
    "Genesis":      macmednafen.MacMednafen("Genesis"),
    # "Dreamcast":    ,
    "Gameboy":      macmednafen.MacMednafen("Gameboy"),
    "GBA":          macmednafen.MacMednafen("GBA"),
}

linux_emulators = {
    # "NES":          ,
    # "SNES":         ,
    # "N64":          ,
    # "Gamecube":     ,
    # "Wii":          ,
    # "PS1":          ,
    # "PS2":          ,
    # "Genesis":      ,
    # "Dreamcast":    ,
    # "Gameboy":      ,
    # "GBA":          ,
    # "DS":           ,
}

emulators = {
    "Windows":  windows_emulators,
    "OSX":      osx_emulators,
    "Linux":    linux_emulators
}

def emulator_exists(platform,console):
    return lookup_emulator(platform,console) is not None
        
def lookup_emulator(platform,console):
    try:
        return emulators[platform][console.shortname]
    except KeyError:
        return None