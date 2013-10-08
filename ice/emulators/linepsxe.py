#!/usr/bin/env python
# encoding: utf-8
"""
linepsxe.py

Created by Marcus Møller.

Represents the GNU/Linux version of the Snes9x emulator
"""

import os

import downloaded_emulator

class LinePSXe(downloaded_emulator.DownloadedEmulator):
    # Information specific to DownloadedEmulator
    _executable_files_ = [os.path.join("linepsxe","epsxe")]
    
    def __init__(self,console_name="ePSXe"):
        super(LinePSXe,self).__init__(console_name)

    def command_string(self,rom):
        # Make sure the script exists before we reference it
        rom.ensure_exe_file_exists()

        # ePSXe requires some parameters, add them as well
        return "\"%s\" -nogui -loadiso \"%s\"" % (self.location,rom.path)
        
    def set_control_scheme(self,controls):
        pass