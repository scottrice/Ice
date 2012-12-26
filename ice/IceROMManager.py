#!/usr/bin/env python
# encoding: utf-8
"""
IceROMManager.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.
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
        
        Stores the managed ROMs in a set for Time Complexity. See
        http://wiki.python.org/moin/TimeComplexity
        for details
        """
        self.shortcut_manager = shortcut_manager
        self.managed_roms = set()
        self.__find_managed_roms_in_previous_shortcuts__()
        
    def __find_managed_roms_in_previous_shortcuts__(self):
        return None
        
    def __shortcut_for_rom__(self,rom):
        # TODO: Support custom icons
        return SteamShortcut(rom.name(),rom.executable(),rom.console.executables_directory(),"",rom.console.fullname)
        
    def add_rom(self,rom):
        if rom.path not in self.managed_roms:
            self.managed_roms.add(rom.path)
            self.shortcut_manager.add(self.__shortcut_for_rom__(rom))