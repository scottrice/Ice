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
import platform
import filesystem_helper
import emulator_manager
from ice_logging import log_file, log_both
from rom import ROM

class Console():
    @classmethod
    def settings_consoles(self):
        consoles = []
        consoles_dict = settings.consoles()
        for name in consoles_dict.keys():
            console_data = consoles_dict[name]
            nickname = name
            if 'nickname' in console_data:
                nickname = console_data['nickname']
            console = Console(nickname, name)
            consoles.append(console)
        return consoles

    def __init__(self,shortname,fullname):
        self.shortname = shortname
        self.fullname = fullname
        self.emulator = emulator_manager.lookup_emulator(self)
        self.__create_directories_if_needed__()
        
    def __repr__(self):
        return self.shortname
        
    def __create_directories_if_needed__(self):
        """
        Creates directories that the console will need if they don't exist yet
        """
        # If the emulator doesn't exist, don't even bother creating the folders
        # for the console
        if self.emulator is None:
            return
        def create_directory_if_needed(dir):
            if not os.path.exists(dir):
                os.makedirs(dir)
        create_directory_if_needed(self.roms_directory())
        # I don't like this, but the console is creating the directory where
        # the emulator is throwing any exes it needs.
        # TODO: Figure out a decent way to put this in the emulator object
        create_directory_if_needed(self.executables_directory())
        
    def roms_directory(self):
        """
        Should return a directory with a decent name for each console, such as
        C:\Users\Scott\Documents\ROMs\N64
        or
        C:\Users\Scott\Documents\ROMs\PS2
        """
        return os.path.join(filesystem_helper.roms_directory(),self.shortname)
        
    def executables_directory(self):
        """
        Should return a directory with a decent name for each emulator, such as
        C:\Users\Scott\Documents\ROMs\N64
        or
        C:\Users\Scott\Documents\ROMs\PS2
        """
        return os.path.join(filesystem_helper.executables_directory(),self.shortname)
        
    def icon_path(self):
        """
        Should return the path to the icon for the given console. This icon
        should be located in the resources/images/icons directory, and should
        be named the same as the emulator shortname with a .png extension
        """
        icon_filename = self.shortname + ".png"
        return os.path.join(filesystem_helper.icons_directory(),icon_filename)
        
    def find_all_roms(self):
        """
        Reads a list of all the ROMs from the appropriate directory for the
        console
        """
        roms = []
        # If the emulator is not functional, we pretend it doesn't have any
        # ROMs
        if not self.emulator.is_functional():
            return roms
        for filename in os.listdir(self.roms_directory()):
            file_path = os.path.join(self.roms_directory(),filename)
            if not os.path.isdir(file_path):
                # On Linux/OSX, we want to make sure hidden files don't get
                # accidently added as well
                if not platform.is_windows() and filename.startswith('.'):
                    continue
                if self.emulator is not None and not self.emulator.valid_rom(file_path):
                    log_file("Ignoring Non-ROM file: %s" % file_path)
                    continue
                roms.append(ROM(file_path,self))
        return roms

def find_all_roms():
    """
    Gets the roms for every console in the list of supported consoles
    """
    all_roms = []
    for console in supported_consoles():
        all_roms.extend(console.find_all_roms())
    return all_roms

def supported_consoles():
    if supported_consoles.cached is None:
        sc = Console.settings_consoles()
        # Remove any consoles from supported_consoles if there does not exist an
        # emulator for them
        for console in list(sc):
            if console.emulator is None:
                sc.remove(console)
            else:
                log_both("Detected Console: %s => %s" % (console.fullname, console.emulator.name))
        # Cache it for next time
        supported_consoles.cached = sc
    return supported_consoles.cached
supported_consoles.cached = None