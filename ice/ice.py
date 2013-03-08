#!/usr/bin/env python

import sys
import os
import inspect

sys.stdout = open("stdout.log","w")
sys.stderr = open("stderr.log","w")

from SteamShortcutManager import SteamShortcutManager
import SteamUserManager
import IceConsole
from IceROMManager import IceROMManager
from IceLogging import log

def main():
    log("=========================Starting Ice")
    # Find the Steam Account that the user would like to add ROMs for
    user_ids = SteamUserManager.user_ids_on_this_machine()
    for user_id in user_ids:
        log("---------------Running for user %s" % str(user_id),2)
        # Load their shortcuts into a SteamShortcutManager object
        shortcuts_path = SteamUserManager.shortcuts_file_for_user_id(user_id)
        shortcuts_manager = SteamShortcutManager(shortcuts_path)
        rom_manager = IceROMManager(shortcuts_manager)
        # Find all of the ROMs that are currently in the designated folders
        roms = IceConsole.find_all_roms()
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
        
if __name__ == "__main__":
    main()