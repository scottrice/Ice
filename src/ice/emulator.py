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

from ice_logging import ice_logger
from persistence.backed_object import BackedObject
import filesystem_helper
import utils

class Emulator(BackedObject):
    backing_store = None

    def __init__(self, identifier):
        super(Emulator, self).__init__(identifier)
        self.name     = identifier
        self.location = self.backed_value('location')
        self.format   = self.backed_value('command', "%l %r")

        self.location = os.path.expanduser(self.location)

        assert self.location is not None, "Missing location for Emulator:`%s`" % identifier
        assert os.path.exists(self.location), "Path `%s` does not exist."

    def __repr__(self):
        return self.name

    def __add_quotes_if_needed__(self, string):
        if string.startswith("\"") and string.endswith("\""):
            return string
        else:
            return "\"%s\"" % string

    def is_enabled(self, verbose=False):
        """
        Checks to see whether enough information has been entered by the user
        to make the emulator useable
        """
        # Right now the only thing we care about is whether a file exists where
        # the user says the emulator is.
        if not os.path.isfile(self.location):
            if verbose:
                ice_logger.log("(Emulator) File does not exist at '%s'. Ignoring %s" % (self.location, self.name))
            return False
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
