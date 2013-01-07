#!/usr/bin/env python
# encoding: utf-8
"""
winbsnes.py

Created by Scott on 2013-01-07.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import downloaded_emulator

class Winbsnes(downloaded_emulator.DownloadedEmulator):

    _download_location_ = "https://dl.dropbox.com/u/2862706/ice_emulators/Winbsnes.zip"
    _relative_exe_path_ = os.path.join("Winbsnes","bsnes.exe")

    def __init__(self,console_name):
        super(Winbsnes,self).__init__(console_name)
        
    def command_string(self,rom):
        """
        Bsnes uses the standard windows command string:
        
        "C:\Path\\to\\bsnes" "C:\Path\\to\ROM"
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)