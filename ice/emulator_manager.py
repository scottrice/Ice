#!/usr/bin/env python
# encoding: utf-8
"""
emulator_manager.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import settings

from emulators import *
from error.config_error import ConfigError
from ice_logging import log_file, log_user

# List of emulators to use for each conole
#
# I was originally going to include a Dreamcast emulator, but none of the
# emulators that I looked at seemed good. The sound especially was super
# buggy. It was most likely because I was on Windows 7, but I want to provide
# a good experience to Win7 as well, so I won't support Dreamcast for now.
#
# I was also originally going to include a Wii emulator, since Dolphin already
# includes Wii support, but it occured to me that the main use case for this
# application was using an Xbox 360 controller with Steam Big Picture, and
# since Wii emulation would require a Wiimote, I figured it didn't make sense
# to include it.
platform = settings.platform_string()
if platform == "Windows":
    emulators = {
        "NES":          winbsnes.Winbsnes("NES"),
        "SNES":         winbsnes.Winbsnes("SNES"),
        "N64":          winproject64.WinProject64("N64"),
        "Gamecube":     windolphin.WinDolphin("Gamecube"),
        "PS1":          winepsxe.WinePSXe("PS1"),
        "PS2":          winpcsx2.WinPCSX2("PS2"),
        "Genesis":      wingens.WinGens("Genesis"),
        "Gameboy":      winbsnes.Winbsnes("Gameboy"),
        "GBA":          winvisualboyadvance.WinVisualBoyAdvance("GBA"),
    }
if platform == "OSX":
    emulators = {
        "NES":          macmednafen.MacMednafen("NES"),
        "SNES":         macsnes9x.MacSnes9x("SNES"),
        # "N64":          ,
        # "Gamecube":     ,
        # "PS1":          ,
        # "PS2":          ,
        "Genesis":      macmednafen.MacMednafen("Genesis"),
        "Gameboy":      macmednafen.MacMednafen("Gameboy"),
        "GBA":          macmednafen.MacMednafen("GBA"),
    }
if platform == "Linux":
    emulators = {
        # "NES":          ,
        # "SNES":         ,
        # "N64":          ,
        # "Gamecube":     ,
        # "PS1":          ,
        # "PS2":          ,
        # "Genesis":      ,
        # "Gameboy":      ,
        # "GBA":          ,
    }

def emulator_platform_prefix(platform):
    return {
        "Windows":  "Win",
        "OSX":      "Mac",
        "Linux":    "Lin",
    }[platform]

def emulator_from_name(emulator_name):
    """Grabs the emulator subclass described by 'emulator_name'. This function
    assumes that an emulator named 'WinProject64' will be in a module called
    'winproject64'."""
    return getattr(globals()[emulator_name.lower()], emulator_name)
        
def lookup_emulator(platform,console):
    emulators_key = platform + ' Emulators' # ex: "Windows Emulators"
    console_key = console.shortname.lower()
    try:
        user_supplied_name = settings.config()[emulators_key][console_key]
        if not user_supplied_name:
            log_file("No user supplied name for %s" % console.shortname)
            return None
        name = emulator_platform_prefix(platform) + user_supplied_name
        return emulator_from_name(name)(console.shortname)
    except KeyError as e:
        # TODO(#28) Throw a ConfigError once it will be caught...
        log_file("Configuration missing key for %s on %s" % (console.shortname, platform))
        return None
    except AttributeError as e:
        # TODO(#28) Throw a ConfigError once it will be caught...
        log_user("Cannot load emulator for %s. Check that your spelling is correct, and that the emulator you request is supported" % console.shortname)
        log_file("Error loading [%s] %s" % (emulator_key, console_key))
        return None