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
from ice.ice_logging import log_both, log_file, log_exception

def main():
    log_both("=========================Starting Ice")
    # Find all of the ROMs that are currently in the designated folders
    roms = console.find_all_roms()
    # Find the Steam Account that the user would like to add ROMs for
    user_ids = steam_user_manager.user_ids_on_this_machine()
    grid_manager = IceGridImageManager()
    for user_id in user_ids:
        log_both("---------------Running for user %s" % str(user_id))
        # Load their shortcuts into a SteamShortcutManager object
        shortcuts_path = steam_user_manager.shortcuts_file_for_user_id(user_id)
        try:
            shortcuts_manager = SteamShortcutManager(shortcuts_path)
        except IOError:
            log_both('No previous shortcuts file found for this user. Skipping them.')
            continue
        rom_manager = IceROMManager(shortcuts_manager)
        # Add the new ROMs in each folder to our Shortcut Manager
        rom_manager.sync_roms(roms)
        # Generate a new shortcuts.vdf file with all of the new additions
        shortcuts_manager.save()
        log_both("---Downloading grid images")
        grid_manager.update_user_images(user_id,roms)
    log_both("=========================Finished")
        
if __name__ == "__main__":
    try:
        main()
    except StandardError as error:
        log_both("####################################")
        log_both("An Error has occurred:")
        log_both(error)
        log_exception()
        log_both("####################################")
    # Keeps the console from closing (until the user hits enter) so they can
    # read any console output
    print "Close the window, or hit enter to exit..."
    raw_input()