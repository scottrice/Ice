#!/usr/bin/env python

import sys
import os

from SteamShortcutManager import SteamShortcutManager
import SteamInstallationLocationManager
import SteamUserManager
import IceConsole
from IceROM import ROM
from IceROMManager import IceROMManager

def main():
    # Find the Steam Account that the user would like to add ROMs for
    user_ids = SteamUserManager.user_ids_on_this_machine()
    for user_id in user_ids:
        # Load their shortcuts into a SteamShortcutManager object
        shortcuts_path = SteamUserManager.shortcuts_file_for_user_id(user_id)
        shortcuts_manager = SteamShortcutManager(shortcuts_path)
        rom_manager = IceROMManager(shortcuts_manager)
        # Find all of the ROMs that are currently in the designated folders
        roms = IceConsole.find_all_roms()
        # Add the new ROMs in each folder to our Shortcut Manager
        for rom in roms:
            # The ROM manager will take care of only adding missing ROMs and
            # such. All changes should be reflected in the shortcuts_manager
            rom_manager.add_rom(rom)
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

def emulator_test():
    nes = IceConsole.console_lookup("NES")
    snes = IceConsole.console_lookup("SNES")
    genesis = IceConsole.console_lookup("Genesis")
    zelda = ROM("/Users/scottrice/ROMs/NES/The Legend of Zelda.nes",nes)
    print nes.emulator.command_string(zelda)
    chrono_trigger = ROM("/Users/scottrice/ROMs/SNES/Chrono Trigger.sfc",snes)
    print snes.emulator.command_string(chrono_trigger)
    sonic = ROM("/Users/scottrice/ROMs/Genesis/Sonic the Hedgehog.md",genesis)
    print genesis.emulator.command_string(sonic)
    

if __name__ == "__main__":
    main()
    # emulator_test()