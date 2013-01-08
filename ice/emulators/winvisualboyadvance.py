#!/usr/bin/env python
# encoding: utf-8
"""
winvisualboyadvance.py

Created by Scott on 2013-01-07.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import downloaded_emulator

class WinVisualBoyAdvance(downloaded_emulator.DownloadedEmulator):
    
    _download_location_ = "https://dl.dropbox.com/u/2862706/ice_emulators/WinVisualBoyAdvance.zip"
    _relative_exe_path_ = os.path.join("WinVisualBoyAdvance","VisualBoyAdvance.exe")

    __invalid_extensions__ = [
        ".sav", # GBA save file
    ]

    def __init__(self,console_name):
        super(WinVisualBoyAdvance,self).__init__(console_name)

    def valid_rom(self,path):
        """
        VisualBoyAdvance does the same thing that bsnes does where it saves your
        save files in the same directory as your ROM. A valid rom is one that
        doesn't have the .sav extension
        """
        # TODO: This code is identical to bsnes code. Look into a refactoring
        romname, romext = os.path.splitext(path)
        if romext in self.__invalid_extensions__:
            return False
        return True
        
    def command_string(self,rom):
        """
        VisualBoyAdvance uses the standard command string format
        
        "C:\Path\\to\VisualBoyAdvance" "C:\Path\\to\ROM"
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)