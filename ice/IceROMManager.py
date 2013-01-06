#!/usr/bin/env python
# encoding: utf-8
"""
IceROMManager.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

The purpose of this class is to handle the interaction (or some would say 
conversion) between ROMs and Steam Shortcuts. This class also handles checking
to make sure I don't add duplicates of any ROMs to Steam.

Functionality should be added to this class if it involves the interaction
between ROMs and Steam Shortcuts.
"""

import sys
import os

import IceFilesystemHelper
from SteamShortcutManager import SteamShortcutManager,SteamShortcut

# Check to see if the directory we are going to use to Store ROMs exists. If it
# does not, then create it.
if not os.path.exists(IceFilesystemHelper.roms_directory()):
    os.makedirs(IceFilesystemHelper.roms_directory())

class IceROMManager():
    def __init__(self,shortcut_manager):
        """
        Takes an already initialized SteamShortcutsManager. Then does a O(n)
        computation to figure out which ROMs from Ice are already present and
        caches that result. That way, adding a ROM to the SteamShortcutsManager
        can be a O(1) lookup to see if the ROM is already managed, and a O(1)
        addition to the list (if it does not exist)
        
        Stores the managed ROMs in a set to optimize time complexity. See
        http://wiki.python.org/moin/TimeComplexity
        for details
        """
        self.shortcut_manager = shortcut_manager
        self.current_shortcut_targets = set()
        for shortcut in self.shortcut_manager.games:
            self.current_shortcut_targets.add(shortcut.exe)
        
    def __shortcut_for_rom__(self,rom):
        # exe_path = "\"%s\"" % rom.executable_path()
        # exe_dir = "\"%s\"" % rom.console.executables_directory()
        command_string = rom.console.emulator.command_string(rom)
        startdir = rom.console.emulator.startdir(rom)
        # Each shortcut should have an icon set based on the console for which
        # it belongs
        return SteamShortcut(rom.name(),command_string,startdir,rom.console.icon_path(),rom.console.fullname)
        
    def add_rom(self,rom):
        # Don't add a ROM if we don't have a supported emulator for it
        if rom.console.emulator is None:
            return
        formatted_executable_path = "\"%s\"" % rom.executable_path()
        # Only add the ROM if it isn't already in Steam
        # if formatted_executable_path not in self.managed_roms:
        
        # We are going to do a funny way of doing this. We will first figure
        # out what the command string would be for this rom, and then we will
        # check to see if there currently exists an identicle string in the
        # shortcuts manager
        command_string = rom.console.emulator.command_string(rom)
        if command_string not in self.current_shortcut_targets:
            print "Adding %s to Steam" % rom.name()
            self.current_shortcut_targets.add(command_string)
            # self.managed_roms.add(formatted_executable_path)
            # Since we are about to add a shortcut for a ROM, we better make
            # sure the executable it needs exists
            # rom.ensure_exe_file_exists()
            self.shortcut_manager.add(self.__shortcut_for_rom__(rom))