"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from pysteam.steam import Steam

from ice.error.config_error import ConfigError

from ice import filesystem_helper as fs
from ice import console
from ice import emulator
from ice import utils
from ice.rom_manager import IceROMManager
from ice.ice_logging import ice_logger

class CommandLineRunner(object):

    def main(self, argv):
        if utils.steam_is_running():
            ice_logger.error("Ice cannot be run while Steam is open. Please close Steam and try again")
            return

        ice_logger.log("Starting Ice")
        ice_logger.log_state_of_the_world(emulator.Emulator.all(), console.Console.all())
        steam = Steam()
        # Find all of the ROMs that are currently in the designated folders
        roms = console.find_all_roms()
        # Find the Steam Account that the user would like to add ROMs for
        users = steam.local_users()
        for user in users:
            ice_logger.log("Running for user %s" % str(user.id32))
            rom_manager = IceROMManager(user)
            rom_manager.sync_roms(roms)
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
