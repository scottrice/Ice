#!/usr/bin/env python
# encoding: utf-8
"""
Emulator.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.

Emulator is the base class of all my emulators.

Functionality should be added here if every single emulator (whether downloaded
or not) would use it
"""

import os
import tempfile
import shutil

from error.config_error import ConfigError
import filesystem_helper

class Emulator(object):
        
    def __init__(self, name, location, format):
        self.name = name
        self.location = os.path.expanduser(location)
        self.format = format
        filesystem_helper.assert_file_exists(self.location, self.__config_error_for_missing_emulator__())

    def __config_error_for_missing_emulator__(self):
        fix = "Cannot read file '%s'. Ensure that the file exists, and that the path is spelled correctly." % self.location
        return ConfigError(self.name, "location", fix, file="emulators.txt")

    def __add_quotes_if_needed__(self, string):
        if string.startswith("\"") and string.endswith("\""):
            return string
        else:
            return "\"%s\"" % string

    def is_functional(self):
        """
        A basic emulator is always functional.
        """
        return True
    
    def command_string(self, rom):
        """Generates a command string using the format specified by the user"""
        # We don't know if the user put quotes around the emulator location. If
        # so, we dont want to add another pair and screw things up.
        quoted_location = self.__add_quotes_if_needed__(self.location)
        # The user didnt give us the ROM information, but screw it, I already
        # have some code to add quotes to a string, might as well use it.
        quoted_rom = self.__add_quotes_if_needed__(rom.path)
        return self.format.replace("%l", quoted_location).replace("%r", quoted_rom)
        
    def startdir(self,rom):
        """
        Returns the directory which stores the emulator. This value is useful
        as the 'StartDir' option of a Steam Shortcut
        """
        return os.path.dirname(self.location)
