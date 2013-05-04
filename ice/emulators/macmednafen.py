#!/usr/bin/env python
# encoding: utf-8
"""
macmednafen.py

Created by Scott on 2013-01-05.
Copyright (c) 2013 Scott Rice. All rights reserved.

Represents the Mac version of the mednafen emulator
"""

import sys
import os

import downloaded_emulator

class MacMednafen(downloaded_emulator.DownloadedEmulator):
    # # Information specific to DownloadedEmulator
    _executable_files_ = [os.path.join("MacMednafen","mednafen")]
    
    def __init__(self,console_name):
        super(MacMednafen,self).__init__(console_name)
    
    def command_string(self,rom):
        """
        The command string for a mednafen game is just
        \"/Location/Of/mednafen\" \"/Location/Of/Rom\"
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)

    def set_control_scheme(self,controls):
        pass