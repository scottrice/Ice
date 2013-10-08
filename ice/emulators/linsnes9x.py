#!/usr/bin/env python
# encoding: utf-8
"""
linsnes9x.py

Created by Marcus Møller.

Represents the GNU/Linux version of the Snes9x emulator
"""

import os

import downloaded_emulator

class LinSnes9x(downloaded_emulator.DownloadedEmulator):
    # Information specific to DownloadedEmulator
    _executable_files_ = [os.path.join("linsnes9x","snes9x")]
    
    def __init__(self,console_name="SNES"):
        super(LinSnes9x,self).__init__(console_name)

    def command_string(self,rom):
        """
        Snes9x has been giving me problems, and I can't seem to run it from 
        Steam directly. Instead, I am going with the old method of creating a
        shell script and having Steam run the shell script
        """
        # Make sure the script exists before we reference it
        rom.ensure_exe_file_exists()
        return "\"%s\"" % (rom.executable_path())
        
    def startdir(self,rom):
        """
        When using old-style scripts, I just return the exectuables directory 
        for the StartDir
        """
        return rom.console.executables_directory()
        
    def set_control_scheme(self,controls):
        pass