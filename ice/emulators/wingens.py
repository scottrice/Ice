#!/usr/bin/env python
# encoding: utf-8
"""
wingens.py

Created by Scott on 2013-01-19.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import downloaded_emulator

class WinGens(downloaded_emulator.DownloadedEmulator):
    
    _download_location_ = "https://dl.dropbox.com/u/2862706/ice_emulators/WinGens.zip"
    # _relative_exe_path_ = os.path.join("WinGens","gens.exe")
    _relative_exe_path_ = os.path.join("WinGens","gens-launcher.exe")
    
    def __init__(self,console_name):
        super(WinGens,self).__init__(console_name)
        
    def command_string(self,rom):
        """
        Gens uses the standard windows command string:
        
        "C:\Path\To\gens" "C:\Path\To\ROM"
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)