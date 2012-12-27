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

class Console():
    def __init__(self,shortname,fullname,emulator):
        self.shortname = shortname
        self.fullname = fullname
        self.emulator = emulator
        
    def path(self):
        """
        Should return a directory with a decent name for each emulator, such as
        C:\Users\Scott\Documents\ROMs\N64
        or
        C:\Users\Scott\Documents\ROMs\PS2
        """
        return os.path.join(IceFilesystemHelper.rom_directory(),self.shortname)
        
    def executables_directory(self):
        """
        Should return a directory with a decent name for each emulator, such as
        C:\Users\Scott\Documents\ROMs\N64
        or
        C:\Users\Scott\Documents\ROMs\PS2
        """
        return os.path.join(IceFilesystemHelper.executables_directory(),self.shortname)
        
    def find_all_roms(self):
        return []

def find_all_roms():
    all_roms = []
    for console in supported_consoles:
        all_roms.extend(console.find_all_roms())
    return all_roms

# TODO: Figure out what should go into the Emulator section. We need some way
# of representing emulators, but is a string enough? Do we need an object?
n64 = Console("N64","Nintendo 64","")
gba = Console("GBA","Gameboy Advance","")

supported_consoles = [
    # nes,
    # snes,
    n64,
    # ps1,
    # ps2,
    # genesis,
    # dreamcast,
    # gameboy,
    gba#,
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