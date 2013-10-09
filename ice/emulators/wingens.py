#!/usr/bin/env python
# encoding: utf-8
"""
wingens.py

Created by Scott on 2013-01-19.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import downloaded_emulator

class WinGens(downloaded_emulator.DownloadedEmulator):
    
    def __init__(self,console_name):
        super(WinGens,self).__init__(console_name)
        
    def command_string(self,rom):
        """
        Gens uses the standard windows command string:
        
        "C:\Path\To\gens" "C:\Path\To\ROM"
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)