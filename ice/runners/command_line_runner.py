"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from ice.error.config_error import ConfigError

from ice.steam_shortcut_manager import SteamShortcutManager

from ice import steam_user_manager
from ice import filesystem_helper as fs
from ice import console
from ice import emulator
from ice.rom_manager import IceROMManager
from ice.process_helper import steam_is_running
from ice.grid_image_manager import IceGridImageManager
from ice.ice_logging import ice_logger

class CommandLineRunner(object):

    def main(self, argv):
        if steam_is_running():
            ice_logger.error("Ice cannot be run while Steam is open. Please close Steam and try again")
            return

        ice_logger.log("Starting Ice")
        ice_logger.log_state_of_the_world(emulator.Emulator.all(), console.Console.all())
        # Find all of the ROMs that are currently in the designated folders
        roms = console.find_all_roms()
        # Find the Steam Account that the user would like to add ROMs for
        user_ids = steam_user_manager.user_ids_on_this_machine()
        grid_manager = IceGridImageManager()
        for user_id in user_ids:
            ice_logger.log("Running for user %s" % str(user_id))
            # Load their shortcuts into a SteamShortcutManager object
            shortcuts_path = steam_user_manager.shortcuts_file_for_user_id(user_id)
            shortcuts_manager = SteamShortcutManager(shortcuts_path)
            rom_manager = IceROMManager(shortcuts_manager)
            # Add the new ROMs in each folder to our Shortcut Manager
            rom_manager.sync_roms(roms)
            # Backup the current shortcuts.vdf file
            shortcuts_manager.backup(user_id)
            # Generate a new shortcuts.vdf file with all of the new additions
            shortcuts_manager.save()
            grid_manager.update_user_images(user_id,roms)
        ice_logger.log('Ice finished')

    def run(self, argv):
      try:
          self.main(argv)
      except ConfigError as error:
          ice_logger.error('Stopping')
          ice_logger.log_config_error(error)
          ice_logger.exception()
      except StandardError as error:
          ice_logger.exception()
      # Keeps the console from closing (until the user hits enter) so they can
      # read any console output
      print ""
      print "Close the window, or hit enter to exit..."
      raw_input()
