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
        self.managed_roms = set()
        self.__find_managed_roms_in_previous_shortcuts__()
        
    # TODO: Implement. Should figure out which shortcuts in the 
    # SteamShortcutManager were added by Ice. Possibly include a flag for that?
    def __find_managed_roms_in_previous_shortcuts__(self):
        return None
        
    def __shortcut_for_rom__(self,rom):
        # TODO: Support custom icons
        exe_path = "\"%s\"" % rom.executable_path()
        exe_dir = "\"%s\"" % rom.console.executables_directory()
        return SteamShortcut(rom.name(),exe_path,exe_dir,"",rom.console.fullname)
        
    def add_rom(self,rom):
        if rom.path not in self.managed_roms:
            self.managed_roms.add(rom.path)
            self.shortcut_manager.add(self.__shortcut_for_rom__(rom))