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
        
    def path_for_config_file(self):
        return os.path.join(self.directory,"User","Config","Dolphin.ini")   
    
    def path_for_input_file(self):
        return os.path.join(self.directory,"User","Config","GCPadNew.ini")
    
    def set_memcard_location(self):
        """
        Sets the location for Dolphin to save the memory card to a non-terrible
        location. This is set normally in Dolphin.ini, which means that if you
        download my pre set-up emulators, the value will be set relative to my
        computer. That is clearly not optimal, so this function changes it based
        on the current environment
        """
        def replacement_function(line):
            try:
                first_space = line.index(' ')
                current_id = line[:first_space]
                if current_id.startswith('Memcard'):
                    memcard_location = os.path.join(self.directory,"User","GC",current_id+".USA.raw")
                    return "%s = %s\n" % (current_id,memcard_location)
            except:
                pass
            return line
        self.replace_contents_of_file(self.path_for_config_file(),replacement_function)
        
    def set_control_scheme(self,controls):
        controls_map = self.identifier_to_control_map()
        def replacement_function(line):
            # The current identifier is everything before the first space
            try:
                first_space = line.index(' ')
                current_id = line[:first_space]
                # Since 'Main Stick' has a space in it, we need to actually
                # split the current id at the SECOND space in that case
                if current_id == "Main":
                    second_space = line.index(' ',first_space+1)
                    current_id = line[:second_space]
                control = controls_map[current_id]
                control_value = controls[control]
                if control_value != "":
                    return "%s = %s\n" % (current_id,control_value)
            except:
                return line
            return line
        self.replace_contents_of_file(self.path_for_input_file(),replacement_function)
        
    def identifier_to_control_map(self):
        return {
            "Device":"device",
            "Buttons/A":"a",
            "Buttons/B":"b",
            "Buttons/X":"x",
            "Buttons/Y":"y",
            "Buttons/Z":"z",
            "Buttons/Start":"start",
            "Main Stick/Up":"up",
            "Main Stick/Down":"down",
            "Main Stick/Left":"left",
            "Main Stick/Right":"right",
            "C-Stick/Up":"c-up",
            "C-Stick/Down":"c-down",
            "C-Stick/Left":"c-left",
            "C-Stick/Right":"c-right",
            "D-Pad/Up":"d-up",
            "D-Pad/Down":"d-down",
            "D-Pad/Left":"d-left",
            "D-Pad/Right":"d-right",
            "Triggers/L":"l",
            "Triggers/R":"r"
        }