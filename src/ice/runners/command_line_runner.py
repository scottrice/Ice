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

    def path_for_data_file(self, filename):
        """
        Returns the path to a data file named `filename`.
        This function first checks to see if the data file exists in the data
        directory. If so, it returns that.
        Then, this function checks to see if the data file exists in the local
        directory. If so, it returns that.
        If neither of those things are true then this function will return the
        path to a new file in the data directory.
        """
        local_path = os.path.abspath(filename)
        data_path = os.path.join(Configuration.data_directory(), filename)
        if os.path.isfile(data_path):
            return data_path
        elif os.path.isfile(local_path):
            return local_path
        else:
            return data_path

    def main(self, argv):
        if utils.steam_is_running():
            ice_logger.error("Ice cannot be run while Steam is open. Please close Steam and try again")
            return

        ice_logger.log("Starting Ice")
        config_data_path    = self.path_for_data_file("config.txt")
        consoles_data_path  = self.path_for_data_file("consoles.txt")
        emulators_data_path = self.path_for_data_file("emulators.txt")
        # TODO: Create any missing directories that Ice will need
        config = Configuration(
            ConfigFileBackingStore(config_data_path),
            ConfigFileBackingStore(consoles_data_path),
            ConfigFileBackingStore(emulators_data_path),
        )
        ice_logger.log_configuration(config)
        steam = Steam()
        # Find all of the ROMs that are currently in the designated folders
        roms = config.valid_roms()
        # Find the Steam Account that the user would like to add ROMs for
        users = steam.local_users()
        for user in users:
            ice_logger.log("=========== User: %s ===========" % str(user.id32))
            rom_manager = IceROMManager(user, config)
            rom_manager.sync_roms(roms)
        ice_logger.log('Ice finished')

    def run(self, argv):
      try:
          self.main(argv)
      except Exception as error:
          ice_logger.exception()
      # Keeps the console from closing (until the user hits enter) so they can
      # read any console output
      print ""
      print "Close the window, or hit enter to exit..."
      raw_input()
