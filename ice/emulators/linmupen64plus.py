#!/usr/bin/env python
# encoding: utf-8
"""
linmupen64plus.py

Created by Marcus Møller.

Represents the GNU/Linux version of the Mupen64Plus emulator
"""

import os

import downloaded_emulator

class LinMupen64Plus(downloaded_emulator.DownloadedEmulator):
    # Information specific to DownloadedEmulator
    _executable_files_ = [os.path.join("linmupen64plus","mupen64plus")]
    
    def __init__(self,console_name="Mupen64Plus"):
        super(LinMupen64Plus,self).__init__(console_name)

    def command_string(self,rom):
        # Make sure the script exists before we reference it
        rom.ensure_exe_file_exists()

        # Mupen64Plus requires some parameters, add them as well
        return "\"%s\" \"%s\"" % (self.location,rom.path)