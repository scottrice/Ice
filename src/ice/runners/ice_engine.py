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
from ice.configuration import Configuration
from ice.error.env_checker_error import EnvCheckerError
from ice.environment_checker import EnvironmentChecker
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

  def validate_base_environment(self):
      """
      Validate that the current environment meets all of Ice's requirements.
      """
      with EnvironmentChecker() as env_checker:
        # If Steam is running then any changes we make will be overwritten
        env_checker.require_program_not_running("Steam")
        # I'm not sure if there are situations where this won't exist, but I
        # assume that it does everywhere and better safe than sorry
        env_checker.require_directory_exists(self.steam.userdata_location())

  def validate_configuration(self, configuration):
      with EnvironmentChecker() as env_checker:
        for console in configuration.console_manager:
          if console.is_enabled():
            # Consoles assume they have a ROMs directory
            env_checker.require_directory_exists(console.roms_directory())

  def validate_user_environment(self, user):
      """
      Validate that the current environment for a given user meets all of
      Ice's requirements.
      """
      with EnvironmentChecker() as env_checker:
        # If the user hasn't added any grid images on their own then this
        # directory wont exist, so we require it explicitly here
        env_checker.require_directory_exists(user.grid_directory())
        # And it needs to be writable if we are going to save images there
        env_checker.require_path_writable(user.grid_directory())

  def main(self):
      self.logger.info("=========== Starting Ice ===========")
      # TODO: Create any missing directories that Ice will need
      self.logger.log_configuration(self.config)
      for user in self.users:
          self.logger.info("=========== User: %s ===========" % str(user.id32))
          self.run_for_user(user)

  def run_for_user(self, user):
      try:
        self.validate_base_environment()
        self.validate_configuration(self.config)
        self.validate_user_environment(user)
      except EnvCheckerError as e:
        self.logger.exception("Ice cannot run because of issues with your system. Please resolve the issues above and try running Ice again")
        return
      # Find all of the ROMs that are currently in the designated folders
      roms = self.config.valid_roms()
      rom_manager = IceROMManager(user, self.config, self.logger)
      rom_manager.sync_roms(roms)

  def run(self):
    try:
        self.main()
    except Exception as error:
        self.logger.exception("An exception occurred while running Ice")
