#!/usr/bin/env python
# encoding: utf-8
"""
windolphin.py

Created by Scott on 2013-01-05.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import downloaded_emulator

class WinDolphin(downloaded_emulator.DownloadedEmulator):
    
    def __init__(self,console_name):
        super(WinDolphin,self).__init__(console_name)
        self.set_memcard_location()
    
    def command_string(self,rom):
        """
        The command string for Dolphin is really easy, it is just
        \"C:\Path\To\Dolphin\" --batch --exec=\"C:\Path\To\ROM\"
        """
        return "\"%s\" --batch --exec=\"%s\"" % (self.location,rom.path)