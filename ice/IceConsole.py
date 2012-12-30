#!/usr/bin/env python
# encoding: utf-8
"""
IceConsole.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

This class represents the Console datatype. Each ROM is associated with a
Console, and each Console has many ROMs. A Console also is associated with an
emulator, which can be used to play a ROM.

Functionality should be added to this class/module if it deals with Consoles or
their emulators. This includes finding a list of ROMs in this console's folder.
"""

import sys
import os

import IceFilesystemHelper
from IceROM import ROM

class Console():
    def __init__(self,shortname,fullname,emulator_path):
        self.shortname = shortname
        self.fullname = fullname
        self.emulator_path = emulator_path
        self.__create_directories_if_needed__()
        
    def __create_directories_if_needed__(self):
        """
        Creates directories that the console will need if they don't exist yet
        """
        def create_directory_if_needed(dir):
            if not os.path.exists(dir):
                os.makedirs(dir)
        create_directory_if_needed(self.roms_directory())
        create_directory_if_needed(self.executables_directory())
        
    def roms_directory(self):
        """
        Should return a directory with a decent name for each console, such as
        C:\Users\Scott\Documents\ROMs\N64
        or
        C:\Users\Scott\Documents\ROMs\PS2
        """
        return os.path.join(IceFilesystemHelper.roms_directory(),self.shortname)
        
    def executables_directory(self):
        """
        Should return a directory with a decent name for each emulator, such as
        C:\Users\Scott\Documents\ROMs\N64
        or
        C:\Users\Scott\Documents\ROMs\PS2
        """
        return os.path.join(IceFilesystemHelper.executables_directory(),self.shortname)
        
    def find_all_roms(self):
        """
        Reads a list of all the ROMs from the appropriate directory for the
        console
        """
        roms = []
        for file in os.listdir(self.roms_directory()):
            if not os.path.isdir(file):
                roms.append(ROM(file,self))
        return roms

def find_all_roms():
    """
    Gets the roms for every console in the list of supported consoles
    """
    all_roms = []
    for console in supported_consoles:
        all_roms.extend(console.find_all_roms())
    return all_roms

# Emulator should be the path leading to the emulator application. Creating an
# exe for a rom then will basically look like "{emulator_path} {rom_path}"
nes = Console("NES","Nintendo Entertainment System","")
n64 = Console("N64","Nintendo 64","/Applications/sixtyforce.app")
gba = Console("GBA","Gameboy Advance","")

supported_consoles = [
    nes,
    # snes,
    n64,
    # ps1,
    # ps2,
    # genesis,
    # dreamcast,
    # gameboy,
    gba,
    # ds
]

# console_mapping is a map between the shortname (which is also used as the
# the folder name) of a console to the console object itself. For example,
# console_mapping["N64"] should return the n64 instance variable (which 
# contains the longname, shortname, emulator path, etc)
console_mapping = {}
for console in supported_consoles:
    console_mapping[console.shortname] = console
    
def console_lookup(name):
    try:
        return console_mapping[name]
    except KeyError:
        return None