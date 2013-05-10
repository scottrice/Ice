#!/usr/bin/env python
# encoding: utf-8
"""
winpcx2.py

Created by Scott on 2013-01-25.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import downloaded_emulator
import bios_emulator

class WinPCSX2(downloaded_emulator.DownloadedEmulator,bios_emulator.BiosEmulator):
    
    _bios_directory_ = "bios"
    _bios_name_ = "scph39001.bin"
    
    def __init__(self,console_name):
        super(WinPCSX2,self).__init__(console_name)
        
    def command_string(self,rom):
        """
        PCSX2 uses the default command string
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)

    def path_for_input_file(self):
        return os.path.join(self.directory,"inis","Lilypad.ini")

    def set_control_scheme(self,controls):
        """
        PCSX2 keeps it's control scheme in a flat file for it's input plugin.
        Since we are using Lilypad, this file is called Lilypad.ini.
        """
        # Lilypad.ini is much more complicated than most of the flat files I've
        # had to deal with. For now, I am just going to worry about letting the
        # user set their preferences on the xbox360 controller. At some point
        # I will have to look into a system that allows the user to use any
        # controller with PCSX2
        def replacement_function(line):
            rf = replacement_function
            # Start of a section
            if line.startswith("["):
                rf.section = line.lstrip("[").rstrip().rstrip("]")
            if rf.section == "Device 13" and line.startswith("Binding"):
                # Figure out the current binding settings
                binding_prefix = line[:line.index('=')+1]
                binding = line[len(binding_prefix):].split(",")
                control_id = self.ini_number_to_control_identifier(binding[2])
                new_value = controls[control_id]
                binding[0] = new_value
                return "%s%s" % (binding_prefix,",".join(binding))
            return line
        replacement_function.section = ""
        self.replace_contents_of_file(self.path_for_input_file(),replacement_function)

    def ini_number_to_control_identifier(self,ini_number):
        """
        Lilypad stores a list of bindings, and the button that is associated
        with a given binding is based off of a number.

        This function returns a map whose keys are the number, and whose values
        are the associated button identifier in controls.txt
        """
        return {
            "16":"select",
            "19":"start",
            "20":"up",
            "21":"right",
            "22":"down",
            "23":"left",
            "24":"l2",
            "25":"r2",
            "26":"l1",
            "27":"r1",
            "28":"triangle",
            "29":"circle",
            "30":"x",
            "31":"square",
            "32":"leftanalog-up",
            "33":"leftanalog-right",
            "34":"leftanalog-down",
            "35":"leftanalog-left",
            "36":"rightanalog-up",
            "37":"rightanalog-right",
            "38":"rightanalog-down",
            "39":"rightanalog-left"
        }[ini_number.strip()]