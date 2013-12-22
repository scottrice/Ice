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
from ice_logging import log_both
import filesystem_helper
import settings
import utils

class Emulator(object):

    @classmethod
    def lookup(self, name):
        for emulator in settings_emulators():
            if emulator.name == name:
                return emulator
        return None

    def __init__(self, name, location, options={}):
        self.name = name
        self.location = os.path.expanduser(location)
        self.format = utils.idx(options, 'command', "%l %r")
        filesystem_helper.assert_file_exists(self.location, self.__config_error_for_missing_emulator__())

    def __config_error_for_missing_emulator__(self):
        fix = "Cannot read file '%s'. Ensure that the file exists, and that the path is spelled correctly." % self.location
        return ConfigError(self.name, "location", fix, file="emulators.txt")

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
                log_both("(Emulator) File does not exist at '%s'. Ignoring %s" % (self.location, self.name))
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

@utils.memoize
def settings_emulators():
    emulators = []
    emulators_dict = settings.emulators()
    for name in emulators_dict.keys():
        emulator_data = emulators_dict[name]
        location = utils.idx(emulator_data, 'location', "")
        current_emulator = Emulator(name, location, emulator_data)
        if current_emulator.is_enabled(verbose=True):
            emulators.append(current_emulator)
    # After all of the invalid emulators have been removed, let the user know
    # which emulators have initialized successfully
    for emulator in emulators:
        log_both("Detected Emulator: %s" % name)
    return emulators
