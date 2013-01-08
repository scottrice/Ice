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

import IceSettings
import IceFilesystemHelper
import IceEmulatorManager
from IceROM import ROM

class Console():
    def __init__(self,shortname,fullname):
        self.shortname = shortname
        self.fullname = fullname
        self.emulator = self.__find_emulator__()
        self.__create_directories_if_needed__()
        
    def __repr__(self):
        return self.shortname
        
    def __find_emulator__(self):
        """
        Uses the settings to determine the emulator path for a given console
        """
        platform = IceSettings.platform_string()
        if not IceEmulatorManager.emulator_exists(platform,self):
            return None
        return IceEmulatorManager.lookup_emulator(platform,self)
        # emulators_dir = IceFilesystemHelper.bundled_emulators_directory(platform)
        # return os.path.join(emulators_dir,IceSettings.relative_emulator_path(platform,self))
        
    def __create_directories_if_needed__(self):
        """
        Creates directories that the console will need if they don't exist yet
        """
        # If the emulator doesn't exist, don't even bother creating the folders
        # for the console
        if not IceEmulatorManager.emulator_exists(IceSettings.platform_string(),self):
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
        return os.path.join(IceFilesystemHelper.roms_directory(),self.shortname)
        
    def executables_directory(self):
        """
        Should return a directory with a decent name for each emulator, such as
        C:\Users\Scott\Documents\ROMs\N64
        or
        C:\Users\Scott\Documents\ROMs\PS2
        """
        return os.path.join(IceFilesystemHelper.executables_directory(),self.shortname)
        
    def icon_path(self):
        """
        Should return the path to the icon for the given console. This icon
        should be located in the resources/images/icons directory, and should
        be named the same as the emulator shortname with a .png extension
        """
        icon_filename = self.shortname + ".png"
        return os.path.join(IceFilesystemHelper.icons_directory(),icon_filename)
        
    def find_all_roms(self):
        """
        Reads a list of all the ROMs from the appropriate directory for the
        console
        """
        roms = []
        for filename in os.listdir(self.roms_directory()):
            file_path = os.path.join(self.roms_directory(),filename)
            if not os.path.isdir(file_path):
                # On Linux/OSX, we want to make sure hidden files don't get
                # accidently added as well
                if IceSettings.platform_string() != "Windows" and filename.startswith('.'):
                    continue
                if self.emulator is not None and not self.emulator.valid_rom(file_path):
                    print "Ignoring Non-ROM file: %s" % file_path
                    continue
                roms.append(ROM(file_path,self))
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
nes = Console("NES","Nintendo Entertainment System")
snes = Console("SNES","Super Nintendo")
n64 = Console("N64","Nintendo 64")
gamecube = Console("Gamecube","Nintendo Gamecube")
wii = Console("Wii", "Nintendo Wii")
ps1 = Console("PS1", "Playstation")
ps2 = Console("PS2", "Playstation 2")
genesis = Console("Genesis", "Sega Genesis")
dreamcast = Console("Dreamcast", "Sega Dreamcast")
gameboy = Console("Gameboy", "Gameboy")
gba = Console("GBA","Gameboy Advance")
ds = Console("DS","Nintendo DS")

supported_consoles = [
    nes,
    snes,
    n64,
    gamecube,
    wii,
    ps1,
    ps2,
    genesis,
    dreamcast,
    gameboy,
    gba,
# I orginally planned DS support, but didn't think it though, as the point
# of this project was to make something controller friendly, and I have no
# idea how someone would use a controller to emulate a Nintendo DS. I can see
# my application being useful without a controller, as a way to get Steam to
# manage ROMs, but for now I will ignore DS support
    # ds
]

# Remove any consoles from supported_consoles if there does not exist an
# emulator for them
for console in list(supported_consoles):
    if not IceEmulatorManager.emulator_exists(IceSettings.platform_string(),console):
        supported_consoles.remove(console)

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