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

import os

import filesystem_helper
from console import Console
from ice_logging import ice_logger
from steam_grid import SteamGrid

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
        self.managed_shortcuts = set()
        for shortcut in self.shortcut_manager.shortcuts:
            if self.__is_managed_by_ice__(shortcut):
                self.managed_shortcuts.add(shortcut)
    
    def __is_managed_by_ice__(self,shortcut):
        """
        We determine whether a shortcut is managed by ice by whether the app
        directory location is contained in the target string. The way I see it,
        a target that uses Ice will either point to an emulator (which is
        contained in the app dir), or to an Ice exectuable (again, contained
        in the Ice dir). Obviously if we add a method of executing roms which
        doesn't involve the app dir, this method will need to be rethought.
        """
        for console in Console.all_enabled():
            if console.roms_directory() in shortcut.exe:
                return True
        return False
        
    def rom_already_in_steam(self,rom):
        """
        To check whether a ROM is already managed by Steam, we generate a
        Shortcut for that ROM, and then figure out whether an equal ROM exists
        in our Shortcut Manager.
        """
        generated_shortcut = rom.to_shortcut()
        return generated_shortcut in self.managed_shortcuts
        
    def add_rom(self,rom):
        # Don't add a ROM if we don't have a supported emulator for it
        if rom.console.emulator is None:
            return
        if not self.rom_already_in_steam(rom):
            ice_logger.log("Adding %s" % rom.name())
            generated_shortcut = rom.to_shortcut()
            self.managed_shortcuts.add(generated_shortcut)
            self.shortcut_manager.add(generated_shortcut)
            
    def remove_deleted_roms_from_steam(self,roms):
        # We define 'has been deleted' by checking whether we have a shortcut
        # that was managed by Ice in Steam that is no longer in our ROM folders
        rom_shortcuts = set()
        for rom in roms:
            rom_shortcuts.add(rom.to_shortcut())
        deleted_rom_shortcuts = self.managed_shortcuts - rom_shortcuts
        for shortcut in deleted_rom_shortcuts:
            ice_logger.log("Deleting: %s" % shortcut.appname)
            self.shortcut_manager.shortcuts.remove(shortcut)
            
    def sync_roms(self,roms):
        """
        Two parts to syncing. 
        1) Remove any ROMs which have been deleted
        2) Add any new ROMs
        """
        # 1)
        self.remove_deleted_roms_from_steam(roms)
        # 2)
        for rom in roms:
            self.add_rom(rom)
            
    def update_artwork(self,user_id,roms):
        # TODO: Implement
        pass
