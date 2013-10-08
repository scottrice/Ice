#!/usr/bin/env python
# encoding: utf-8
"""
winproject64.py

Created by Scott on 2013-01-07.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

if sys.platform.startswith('win'):
    import _winreg as registry

import downloaded_emulator

class WinProject64(downloaded_emulator.DownloadedEmulator):
    
    def __init__(self,console_name):
        super(WinProject64,self).__init__(console_name)
    
    def command_string(self,rom):
        """
        The command string format for Project 64 is just...
        \"C:\Path\To\Project64\" C:\Path\To\ROM
        
        Notice the quotes around the path to Project 64, but the lack of quotes
        around the path to the ROM. This is intended in PJ64 1.6.
        
        Since we need to get the keybindings correct, Project64 needs a 
        launcher. The launcher has no such qualms about quotes, and so the
        standard
        \"C:\Path\To\Project64\" \"C:\Path\To\ROM\"
        
        works fine
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)