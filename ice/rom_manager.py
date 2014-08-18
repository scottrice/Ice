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
from settings import config
from steam_grid import SteamGrid

# Providers
from gridproviders import local_provider
from gridproviders import consolegrid_provider

class IceROMManager():
    def __init__(self, user):
        self.user = user
        self.providers = [
            local_provider.LocalProvider(),
            consolegrid_provider.ConsoleGridProvider(),
        ]

        self.managed_shortcuts = set()
        for shortcut in self.user.shortcuts:
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
            self.user.shortcuts.append(generated_shortcut)
            
    def remove_deleted_roms_from_steam(self,roms):
        # We define 'has been deleted' by checking whether we have a shortcut
        # that was managed by Ice in Steam that is no longer in our ROM folders
        rom_shortcuts = set()
        for rom in roms:
            rom_shortcuts.add(rom.to_shortcut())
        deleted_rom_shortcuts = self.managed_shortcuts - rom_shortcuts
        for shortcut in deleted_rom_shortcuts:
            ice_logger.log("Deleting: %s" % shortcut.name)
            self.user.shortcuts.remove(shortcut)
            
    def sync_roms(self,roms):
        """
        This function takes care of syncing ROMs. After this function exits,
        Steam will contain only non-Ice shortcuts and the ROMs represented
        by `roms`. To accomplish this, the function follows a few steps

        1) Back up shortcuts.vdf file
        2) Remove any ROMs which have been deleted
        3) Add any new ROMs which weren't there previously
        4) Save the changes to shortcuts.vdf
        5) Download artwork for all of the new ROMs
        """
        # Backup the shortcuts before we touch anything
        backup_path = config.shortcuts_backup_path(self.user)
        self.user.save_shortcuts(backup_path)
        # Remove old ROMs
        self.remove_deleted_roms_from_steam(roms)
        # Add new ROMs
        for rom in roms:
            self.add_rom(rom)
        # Save our changes
        self.user.save_shortcuts()
        # Grab new artwork
        self.update_artwork(roms)

    def update_artwork(self,roms):
        """
        Sets a suitable grid image for every rom in 'roms' for `user`
        """
        grid = SteamGrid(self.user.userdata_directory())
        for rom in roms:
            shortcut = rom.to_shortcut()
            if not grid.existing_image_for_filename(grid.filename_for_shortcut(shortcut.name, shortcut.exe)):
                path = self.image_for_rom(rom)
                if path is None:
                    # TODO: Tell the user what went wrong
                    pass
                else:
                    # TODO: Tell the user that an image was found
                    ice_logger.log("Found grid image for %s" % shortcut.name)
                    grid.set_image_for_shortcut(path, shortcut.name, shortcut.exe)

    def image_for_rom(self, rom):
        """
        Goes through each provider until one successfully finds an image.
        Returns None if no provider was able to find an image
        """
        for provider in self.providers:
            (path, error) = provider.image_for_rom(rom)
            if path is not None:
                return path
            # TODO: Log the error for the provider
            ice_logger.debug(error)
        return None