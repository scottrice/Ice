#!/usr/bin/env python
# encoding: utf-8
"""
winvisualboyadvance.py

Created by Scott on 2013-01-07.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import downloaded_emulator

class WinVisualBoyAdvance(downloaded_emulator.DownloadedEmulator):

    __invalid_extensions__ = [
        ".sav", # GBA save file
    ]

    def __init__(self,console_name):
        super(WinVisualBoyAdvance,self).__init__(console_name)

    def valid_rom(self,path):
        """
        VisualBoyAdvance does the same thing that bsnes does where it saves your
        save files in the same directory as your ROM. A valid rom is one that
        doesn't have the .sav extension
        """
        # TODO: This code is identical to bsnes code. Look into a refactoring
        romname, romext = os.path.splitext(path)
        if romext in self.__invalid_extensions__:
            return False
        return True
        
    def command_string(self,rom):
        """
        VisualBoyAdvance uses the standard command string format
        
        "C:\Path\\to\VisualBoyAdvance" "C:\Path\\to\ROM"
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)
    
    def config_path(self):
        return os.path.join(self.directory,"vba.ini")

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
            "Joy0_Up":"up",
            "Joy0_Down":"down",
            "Joy0_Left":"left",
            "Joy0_Right":"right",
            "Joy0_A":"a",
            "Joy0_B":"b",
            "Joy0_L":"l",
            "Joy0_R":"r",
            "Joy0_Select":"select",
            "Joy0_Start":"start",
        }