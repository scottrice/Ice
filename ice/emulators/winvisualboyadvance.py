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

    def __init__(self,console_name):
        super(WinVisualBoyAdvance,self).__init__(console_name)
        
    def command_string(self,rom):
        """
        VisualBoyAdvance uses the standard command string format
        
        "C:\Path\\to\VisualBoyAdvance" "C:\Path\\to\ROM"
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)