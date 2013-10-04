#!/usr/bin/env python

import sys
import os
import inspect

from ice.error.config_error import ConfigError

from ice.steam_shortcut_manager import SteamShortcutManager

from ice import steam_installation_location_manager
from ice import steam_user_manager
from ice import settings
from ice import console
from ice.rom import ROM
from ice.rom_manager import IceROMManager
from ice.grid_image_manager import IceGridImageManager
from ice.ice_logging import log_both, log_file, log_user, log_exception

def main():
    log_both("=========================Starting Ice")
    if steam_running():
        log_both("####################################")
        log_both("An Error has occurred:")
        log_both("Steam seems to be running. Please shutdown Steam before running Ice!")
        sys.exit()

    # Find all of the ROMs that are currently in the designated folders
    roms = console.find_all_roms()
    # Find the Steam Account that the user would like to add ROMs for
    user_ids = steam_user_manager.user_ids_on_this_machine()
    grid_manager = IceGridImageManager()
    for user_id in user_ids:
        log_both("---------------Running for user %s" % str(user_id))
        # Load their shortcuts into a SteamShortcutManager object
        shortcuts_path = steam_user_manager.shortcuts_file_for_user_id(user_id)
        shortcuts_manager = SteamShortcutManager(shortcuts_path)
        rom_manager = IceROMManager(shortcuts_manager)
        # Add the new ROMs in each folder to our Shortcut Manager
        rom_manager.sync_roms(roms)
        # Generate a new shortcuts.vdf file with all of the new additions
        shortcuts_manager.save()
        if IceGridImageManager.should_download_images():
            log_both("---Downloading grid images")
            grid_manager.update_user_images(user_id,roms)
        else:
            log_both("Skipping 'Download Image' step")
    log_both("=========================Finished")

def steam_running():
    # use psutil to loop through all processes and see if steam is running
    try:
        import psutil

        for process in psutil.process_iter():
            if process.name.lower() == "steam.exe" or process.name.lower() == "steam": # Windows, Linux process name - need Mac
                return True

    except ImportError:
        # psutil isnt installed, dont check
        return

if __name__ == "__main__":
    try:
        main()
    except ConfigError as error:
        log_user("=========================Stopping\n")
        log_file("!!!Error was Users' fault. Don't worry about it")
        log_both("There was a problem with '[%s] %s' in config.txt" % (error.section, error.key))
        log_both(error.fix_instructions)
        log_file("!!!")
    except StandardError as error:
        log_both("####################################")
        log_both("An Error has occurred:")
        log_both(error)
        log_exception()
        log_both("####################################")
    # Keeps the console from closing (until the user hits enter) so they can
    # read any console output
    print ""
    print "Close the window, or hit enter to exit..."
    raw_input()