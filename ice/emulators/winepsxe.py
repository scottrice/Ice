#!/usr/bin/env python
# encoding: utf-8
"""
WinePSXe.py

Created by Scott on 2013-01-25.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys

if sys.platform.startswith('win'):
    import _winreg as registry

import downloaded_emulator
import bios_emulator

class WinePSXe(downloaded_emulator.DownloadedEmulator,bios_emulator.BiosEmulator):
    
    _bios_directory_ = "bios"
    _bios_name_ = "SCPH1001.BIN"
    
    def __init__(self,console_name):
        super(WinePSXe,self).__init__(console_name)

    def command_string(self,rom):
        """
        ePSXe uses a normal command string with two flags, the first is nogui,
        which gets rid of the extra window that ePSXe uses to let the user pick
        a ROM from their computer (not needed for us), and the second is
        loadiso, which tells ePSXe to load the game from a file on the users
        computer.
        """
        return "\"%s\" -nogui -loadiso \"%s\"" % (self.location,rom.path)