#!/usr/bin/env python
# encoding: utf-8
"""
linmednafen.py

Created by Marcus Møller.

Represents the GNU/Linux version of the Mednafen emulator
"""

import os

import downloaded_emulator

class LinMednafen(downloaded_emulator.DownloadedEmulator):
    # Information specific to DownloadedEmulator
    _executable_files_ = [os.path.join("linmednafen","mednafen")]
    
    def __init__(self,console_name="Mednafen"):
        super(LinMednafen,self).__init__(console_name)

    def command_string(self,rom):
        # Make sure the script exists before we reference it
        rom.ensure_exe_file_exists()
        return "\"%s\"" % (rom.executable_path())
        
    def startdir(self,rom):
        """
        When using old-style scripts, I just return the exectuables directory 
        for the StartDir
        """
        return rom.console.executables_directory()