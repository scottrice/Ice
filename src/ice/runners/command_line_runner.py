"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import os
from pysteam.steam import Steam

from ice import console
from ice import emulator
from ice import filesystem_helper as fs
from ice import utils
from ice.configuration import Configuration
from ice.ice_logging import ice_logger
from ice.persistence.config_file_backing_store import ConfigFileBackingStore
from ice.rom_manager import IceROMManager

class CommandLineRunner(object):

    def __init__(self):
        config_data_path    = Configuration.path_for_data_file("config.txt")
        consoles_data_path  = Configuration.path_for_data_file("consoles.txt")
        emulators_data_path = Configuration.path_for_data_file("emulators.txt")
        self.config = Configuration(
            ConfigFileBackingStore(config_data_path),
            ConfigFileBackingStore(consoles_data_path),
            ConfigFileBackingStore(emulators_data_path),
        )
        steam = Steam()
        self.users = steam.local_users()

    def main(self, argv):
        ice_logger.log("=========== Starting Ice ===========")
        # TODO: Create any missing directories that Ice will need
        ice_logger.log_configuration(self.config)
        for user in self.users:
            self.run_for_user(user)

    def run_for_user(self, user):
        ice_logger.log("=========== User: %s ===========" % str(user.id32))
        # Find all of the ROMs that are currently in the designated folders
        roms = self.config.valid_roms()
        rom_manager = IceROMManager(user, self.config)
        rom_manager.sync_roms(roms)

    def run(self, argv):
      try:
          if utils.steam_is_running():
              ice_logger.error("Ice cannot be run while Steam is open. Please close Steam and try again")
              return
          self.main(argv)
      except Exception as error:
          ice_logger.exception()
      # Keeps the console from closing (until the user hits enter) so they can
      # read any console output
      print ""
      print "Close the window, or hit enter to exit..."
      raw_input()
