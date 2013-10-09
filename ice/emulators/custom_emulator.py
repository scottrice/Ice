#!/usr/bin/env python
# encoding: utf-8
"""
custom_emulator.py

Created by Scott on 2013-10-06.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import emulator

class CustomEmulator(emulator.Emulator):

    def __init__(self, name, location, format):
        self.name = name
        self.location = location
        self.format = format

    def __repr__(self):
        return "Custom Emulator %s, located at %s" % (self.name, self.location)

    def command_string(self, rom):
        """Generates a command string using the format specified by the user"""
        # We don't know if the user put quotes around the emulator location. If
        # so, we dont want to add another pair and screw things up.
        quoted_location = self.__add_quotes_if_needed__(os.path.expanduser(self.location))
        # The user didnt give us the ROM information, but screw it, I already
        # have some code to add quotes to a string, might as well use it.
        quoted_rom = self.__add_quotes_if_needed__(rom.path)
        return self.format.replace("%l", quoted_location).replace("%r", quoted_rom)

    def __add_quotes_if_needed__(self, string):
        if string.startswith("\"") and string.endswith("\""):
            return string
        else:
            return "\"%s\"" % string
