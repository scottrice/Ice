"""
IceEngine

The job of this class is to perform the functionality that Ice is defined by.
By that I mean the high level goal of `Adding ROMs to Steam`.
"""

import os
from pysteam.steam import Steam

from ice import console
from ice import emulator
from ice import filesystem_helper as fs
from ice import utils
from ice.configuration import Configuration
from ice.ice_logging import IceLogger
from ice.persistence.config_file_backing_store import ConfigFileBackingStore
from ice.rom_manager import IceROMManager

class IceEngine(object):

  def __init__(self):
      self.logger = IceLogger()
      self.logger.debug("Initializing Ice")
      config_data_path    = Configuration.path_for_data_file("config.txt")
      consoles_data_path  = Configuration.path_for_data_file("consoles.txt")
      emulators_data_path = Configuration.path_for_data_file("emulators.txt")
      self.config = Configuration(
          ConfigFileBackingStore(config_data_path),
          ConfigFileBackingStore(consoles_data_path),
          ConfigFileBackingStore(emulators_data_path),
      )
      self.steam = Steam()
      # TODO: Query the list of users some other way
      self.users = self.steam.local_users()

  def main(self):
      self.logger.info("=========== Starting Ice ===========")
      # TODO: Create any missing directories that Ice will need
      self.logger.log_configuration(self.config)
      for user in self.users:
          self.logger.info("=========== User: %s ===========" % str(user.id32))
          self.run_for_user(user)

  def run_for_user(self, user):
      # Find all of the ROMs that are currently in the designated folders
      roms = self.config.valid_roms()
      rom_manager = IceROMManager(user, self.config, self.logger)
      rom_manager.sync_roms(roms)

  def run(self):
    try:
        if utils.steam_is_running():
            self.logger.error("Ice cannot be run while Steam is open. Please close Steam and try again")
            return
        self.main()
    except Exception as error:
        self.logger.exception("An exception occurred while running Ice")
