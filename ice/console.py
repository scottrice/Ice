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
	        extensions = ""
	        if 'extensions' in console_data:
		        extensions = console_data['extensions']
            console = Console(nickname, name, extensions)
            consoles.append(console)
        return consoles

    def __init__(self,shortname,fullname,extensions):
        self.shortname = shortname
        self.fullname = fullname
	self.extensions = extensions
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
        
    def roms_directory(self):
        """
        Should return a directory with a decent name for each console, such as
        C:\Users\Scott\Documents\ROMs\N64
        or
        C:\Users\Scott\Documents\ROMs\PS2
        """
        return os.path.join(filesystem_helper.roms_directory(),self.shortname)
      
    def valid_rom(self,path):
        """
        This function determines if a given path is actually a valid ROM file.
        If a list of extensions is supplied for this console, we check if the path has a valid extension
	    If no extensions are defined for this console, we just accept any file
        """
	log_both("valid extensions are %s" % self.extensions)

	if self.extensions == "":
	        return True
	return any(path.lower().endswith('.'+x) for x in self.extensions.split(' '))
  
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
                if not pf.is_windows() and filename.startswith('.'):
                    continue
                if self.emulator is not None and not self.valid_rom(file_path):
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
