#!/usr/bin/env python

import sys
import os

from SteamShortcutManager import SteamShortcutManager
import SteamInstallationLocationManager
import SteamUserManager
import IceConsole
from IceROM import ROM
from IceROMManager import IceROMManager

manager = SteamShortcutManager()
rom_manager = IceROMManager(manager)
# print SteamUserManager.name_from_communityid64(76561198000852103)
# print "------------------------"
# print SteamUserManager.communityid64_from_name("meris608")
# print "------------------------"
# print SteamUserManager.communityid32_from_name("meris608")
# print "------------------------"
# print SteamUserManager.userdata_directory_for_user_id("40586375")
# print "------------------------"
# print IceFilesystemHelper.executables_directory()


def main():
    # Find the Steam Account that the user would like to add ROMs for
    #user_ids = SteamUserManager.user_ids_on_this_machine()
    user_ids = []
    for user_id in user_ids:
        # Load their shortcuts into a SteamShortcutManager object
        shortcuts_path = SteamUserManager.shortcuts_file_for_user_id(user_id)
        shortcuts_manager = SteamShortcutManager(shortcuts_path)
        rom_manager = IceROMManager(managed)
        # Find all of the ROMs that are currently in the designated folders
        roms = IceConsole.find_all_roms()
        # Add the new ROMs in each folder to our Shortcut Manager
        for rom in roms:
            # The ROM manager will take care of only adding missing ROMs and
            # such. All changes should be reflected in the shortcuts_manager
            rom_manager.add_rom(rom)
        # Generate a new shortcuts.vdf file with all of the new additions
        shortcuts_manager.save()
    
if __name__ == "__main__":
    main()