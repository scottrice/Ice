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
        # managed_roms is a set of executable paths. I chose executable_paths
        # because it should be unique to every rom, and it is something that
        # is easily accessed from both the ROM object and the Shortcut object
        self.managed_roms = set()
        self.__find_managed_roms_in_previous_shortcuts__()
        
    def __find_managed_roms_in_previous_shortcuts__(self):
        """
        We are going to detect if something is managed by Ice by checking
        to see if the executable is inside of Ices executable directory.
        Since there are two layers to the path, {ice_exe_dir}/{console}/{rom},
        and I want to check equality on ice_exe_dir, I need to do two 
        os.path.dirname's. As a shortcut, I could instead do an os.path.dirname
        on the shortcuts startdir, which is always the directory containing the
        ROM.
        """
        for shortcut in self.shortcut_manager.games:
            containing_dir = os.path.dirname(shortcut.startdir)
            # This is required because the shortcut for a rom is the path to
            # the exe surrounded by quotes. Doing a dirname on "\"{dir}\"" will
            # give us "\"{dir}", so we add a leading quote to the executables
            # directory and compare against that
            formatted_exes_directory = "\"%s" % IceFilesystemHelper.executables_directory()
            if containing_dir == formatted_exes_directory:
                self.managed_roms.add(shortcut.exe)
        
    def __shortcut_for_rom__(self,rom):
        # TODO: Support custom icons
        exe_path = "\"%s\"" % rom.executable_path()
        exe_dir = "\"%s\"" % rom.console.executables_directory()
        return SteamShortcut(rom.name(),exe_path,exe_dir,"",rom.console.fullname)
        
    def add_rom(self,rom):
        formatted_executable_path = "\"%s\"" % rom.executable_path()
        # Only add the ROM if it isn't already in Steam
        if formatted_executable_path not in self.managed_roms:
            self.managed_roms.add(formatted_executable_path)
            # Since we are about to add a shortcut for a ROM, we better make
            # sure the executable it needs exists
            rom.ensure_exe_file_exists()
            self.shortcut_manager.add(self.__shortcut_for_rom__(rom))