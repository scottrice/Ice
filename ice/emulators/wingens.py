#!/usr/bin/env python
# encoding: utf-8
"""
wingens.py

Created by Scott on 2013-01-19.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import downloaded_emulator

class WinGens(downloaded_emulator.DownloadedEmulator):
    
    _download_location_ = "https://dl.dropbox.com/u/2862706/ice_emulators/WinGens.zip"
    _relative_exe_path_ = os.path.join("WinGens","gens-launcher.exe")
    
    def __init__(self,console_name):
        super(WinGens,self).__init__(console_name)
        
    def command_string(self,rom):
        """
        Gens uses the standard windows command string:
        
        "C:\Path\To\gens" "C:\Path\To\ROM"
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)
        
    def config_path(self):
        return os.path.join(self.directory,"gens.cfg")
        
    def set_control_scheme(self,controls):
        control_map = self.identifier_to_control_map()
        def replacement_function(line):
            try:
                control_identifier = line[:line.index('=')]
                control = control_map[control_identifier]
                control_value = controls[control]
                if control_value != "":
                    return "%s=%s\n" % (control_identifier,control_value)
            except:
                return line
        self.replace_contents_of_file(self.config_path(),replacement_function)
        
    def identifier_to_control_map(self):
        return {
            "P1.Up":"up",
            "P1.Down":"down",
            "P1.Left":"left",
            "P1.Right":"right",
            "P1.Start":"start",
            "P1.A":"a",
            "P1.B":"b",
            "P1.C":"c"
        }