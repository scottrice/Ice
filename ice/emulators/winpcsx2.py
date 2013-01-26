#!/usr/bin/env python
# encoding: utf-8
"""
winpcx2.py

Created by Scott on 2013-01-25.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import downloaded_emulator
import bios_emulator

class WinPCSX2(downloaded_emulator.DownloadedEmulator,bios_emulator.BiosEmulator):
    
    _download_location_ = "https://dl.dropbox.com/u/2862706/ice_emulators/WinPCSX2.zip"
    _relative_exe_path_ = os.path.join("WinPCSX2","pcsx2-launcher.exe")
    _bios_directory_ = "bios"
    _bios_name_ = "scph39001.bin"
    
    def __init__(self,console_name):
        super(WinPCSX2,self).__init__(console_name)
        
    def command_string(self,rom):
        """
        PCSX2 uses the default command string
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)
