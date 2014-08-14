#!/usr/bin/env python
# encoding: utf-8
"""
console.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

This class represents the Console datatype. Each ROM is associated with a
Console, and each Console has many ROMs. A Console also is associated with an
emulator, which can be used to play a ROM.

Functionality should be added to this class/module if it deals with Consoles or
their emulators. This includes finding a list of ROMs in this console's folder.
"""

import os

import settings
import platform_helper as pf
import filesystem_helper
import utils
from ice_logging import ice_logger
from emulator import Emulator
from rom import ROM

class Console():

    def __init__(self, name, options={}):
        self.fullname = name
        self.shortname = utils.idx(options, 'nickname', name)
        self.extensions = utils.idx(options, 'extensions', "")
        self.custom_roms_directory = utils.idx(options, 'roms directory', None)
        self.prefix = utils.idx(options, 'prefix', "")
        self.icon = os.path.expanduser(utils.idx(options, 'icon', ""))
        self.images_directory = os.path.expanduser(utils.idx(options, 'images directory', ""))

        self.emulator = Emulator.lookup(utils.idx(options, 'emulator', ""))
        
    def __repr__(self):
        return self.shortname

    def is_enabled(self,verbose=False):
        if self.emulator is None:
            if verbose:
                ice_logger.log("Skipping %s (no emulator provided)" % self)
            return False
        if self.custom_roms_directory and not filesystem_helper.available_to_use(self.custom_roms_directory, create_if_needed=True):
            if verbose:
                ice_logger.log("Skipping %s (ROMs directory provided either doesn't exist or is not writable)" % self)
            return False
        return True

    def roms_directory(self):
        """
        If the user has specified a ROMs directory in consoles.txt and it is
        accessible to Ice, returns that.

        Otherwise, appends the shortname of the console to the default ROMs
        directory given by config.txt.
        """
        if self.custom_roms_directory:
            return self.custom_roms_directory
        return os.path.join(filesystem_helper.roms_directory(),self.shortname)
      
    def is_valid_rom(self,path):
        """
        This function determines if a given path is actually a valid ROM file.
        If a list of extensions is supplied for this console, we check if the path has a valid extension
        If no extensions are defined for this console, we just accept any file
        """

        if self.extensions == "":
            return True
        extension = os.path.splitext(path)[1].lower()
        return any(extension == ('.'+x.strip().lower()) for x in self.extensions.split(','))
  
    def find_roms(self):
        """
        Reads a list of all the ROMs from the appropriate directory for the
        console
        """
        roms = []
        if not os.path.exists(self.roms_directory()):
            ice_logger.log("Creating %s directory at %s" % (self.shortname,self.roms_directory()))
            os.makedirs(self.roms_directory())
        for filename in os.listdir(self.roms_directory()):
            file_path = os.path.join(self.roms_directory(),filename)
            if not os.path.isdir(file_path):
                # On Linux/OSX, we want to make sure hidden files don't get
                # accidently added as well
                if not pf.is_windows() and filename.startswith('.'):
                    continue
                if self.emulator is not None and not self.is_valid_rom(file_path):
                    ice_logger.warning("Ignoring Non-ROM file: %s" % file_path)
                    continue
                roms.append(ROM(file_path,self))
        return roms

@utils.memoize
def find_all_roms():
    """
    Gets the roms for every console in the list of supported consoles
    """
    all_roms = []
    for console in supported_consoles():
        all_roms.extend(console.find_roms())
    return all_roms

@utils.memoize
def user_defined_consoles():
    consoles = []
    consoles_dict = settings.consoles()
    for name in consoles_dict.keys():
        console_data = consoles_dict[name]
        console = Console(name, console_data)
        consoles.append(console)
    return consoles

@utils.memoize
def supported_consoles():
    consoles = user_defined_consoles()
    # Remove any consoles from supported_consoles if there does not exist an
    # emulator for them
    for console in list(consoles):
        if not console.is_enabled(verbose=True):
            consoles.remove(console)
    # Print out all of the detected consoles so the user knows what is going
    # on.
    for console in consoles:
        ice_logger.log("Detected Console: %s => %s" % (console.fullname, console.emulator.name))
    return consoles
