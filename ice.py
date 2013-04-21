#!/usr/bin/env python

import sys
import os
import inspect

from ice.steam_shortcut_manager import SteamShortcutManager

from ice import steam_installation_location_manager
from ice import steam_user_manager
from ice import settings
from ice import console
from ice.rom import ROM
from ice.rom_manager import IceROMManager
from ice.grid_image_manager import IceGridImageManager
from ice.ice_logging import log

def main():
    log("=========================Starting Ice",2)
    # Find all of the ROMs that are currently in the designated folders
    roms = console.find_all_roms()
    # Find the Steam Account that the user would like to add ROMs for
    user_ids = steam_user_manager.user_ids_on_this_machine()
    grid_manager = IceGridImageManager()
    for user_id in user_ids:
        log("---------------Running for user %s" % str(user_id),2)
        # Load their shortcuts into a SteamShortcutManager object
        shortcuts_path = steam_user_manager.shortcuts_file_for_user_id(user_id)
        shortcuts_manager = SteamShortcutManager(shortcuts_path)
        rom_manager = IceROMManager(shortcuts_manager)
        # Add the new ROMs in each folder to our Shortcut Manager
        rom_manager.sync_roms(roms)
        # For testing purposes, uncomment this code, which will save the new
        # shortcuts.vdf file in updated_shortcuts.vdf instead of overwriting
        # the old file
        # 
        # shortcuts_dir = os.path.dirname(shortcuts_path)
        # my_path = os.path.join(shortcuts_dir,"updated_shortcuts.vdf")
        # shortcuts_manager.save(my_path)
        # 
        # Generate a new shortcuts.vdf file with all of the new additions
        shortcuts_manager.save()
        log("---Downloading grid images",2)
        grid_manager.update_user_images(user_id,roms)
    log("=========================Finished",2)
        
if __name__ == "__main__":
    main()
    # Keeps the console from closing (until the user hits enter) so they can
    # read any console output
    raw_input()