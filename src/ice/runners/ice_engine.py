"""
IceEngine

The job of this class is to perform the functionality that Ice is defined by.
By that I mean the high level goal of `Adding ROMs to Steam`.
"""

import os
from pysteam.steam import Steam

from ice import console
from ice import emulator
from ice.configuration import Configuration
from ice.error.env_checker_error import EnvCheckerError
from ice.environment_checker import EnvironmentChecker
from ice.filesystem import Filesystem
from ice.gridproviders.combined_provider import CombinedProvider
from ice.gridproviders.consolegrid_provider import ConsoleGridProvider
from ice.gridproviders.local_provider import LocalProvider
from ice.history.managed_rom_archive import ManagedROMArchive
from ice.ice_logging import IceLogger
from ice.parsing.rom_parser import ROMParser
from ice.persistence.config_file_backing_store import ConfigFileBackingStore
from ice.rom_finder import ROMFinder
from ice.steam_grid_updater import SteamGridUpdater
from ice.steam_shortcut_synchronizer import SteamShortcutSynchronizer

def _path_with_override(path_override, default_name):
  if path_override is not None:
    return path_override
  return Configuration.path_for_data_file(default_name)

class IceEngine(object):

  def __init__(self, options):
    """Valid options for creating an IceEngine are as follows:

    * config    - The path to the config file to use. Searches the default paths
                  for 'config.txt' otherwise
    * consoles  - The path to the consoles file to use. Searches the default
                  paths for 'consoles.txt' if none is provided
    * emulators - The path to the emulators file to use. Searches the default
                  paths for 'emulators.txt' if none is provided
    * verbose   - Turn on debug logging.
    """
    self.validated_base_environment = False
    self.validated_configuration = False
    self.logger = IceLogger(verbose=options.verbose)
    self.logger.debug("Initializing Ice")
    config_data_path = _path_with_override(options.config, "config.txt")
    consoles_data_path = _path_with_override(options.consoles, "consoles.txt")
    emulators_data_path = _path_with_override(options.emulators, "emulators.txt")
    self.config = Configuration(
        ConfigFileBackingStore(config_data_path),
        ConfigFileBackingStore(consoles_data_path),
        ConfigFileBackingStore(emulators_data_path),
    )
    self.steam = Steam()
    # TODO: Query the list of users some other way
    self.users = self.steam.local_users()

    filesystem = Filesystem()
    parser = ROMParser(self.logger)
    self.rom_finder = ROMFinder(self.config, filesystem, parser)
    archive_data_path = Configuration.path_for_data_file("archive.json")
    managed_rom_archive = ManagedROMArchive(archive_data_path)
    self.shortcut_synchronizer = SteamShortcutSynchronizer(managed_rom_archive, self.logger)

    provider = CombinedProvider(
        LocalProvider(self.logger),
        ConsoleGridProvider(self.logger),
    )
    self.grid_updater = SteamGridUpdater(provider, self.logger)

  def validate_base_environment(self):
    """
    Validate that the current environment meets all of Ice's requirements.
    """
    if self.validated_base_environment:
      return
    with EnvironmentChecker() as env_checker:
      # If Steam is running then any changes we make will be overwritten
      env_checker.require_program_not_running("Steam")
      # I'm not sure if there are situations where this won't exist, but I
      # assume that it does everywhere and better safe than sorry
      env_checker.require_directory_exists(self.steam.userdata_location())
      # This is used to store history information and such
      env_checker.require_directory_exists(Configuration.data_directory())
    self.validated_base_environment = True

  def validate_configuration(self, configuration):
    if self.validated_configuration:
      return
    with EnvironmentChecker() as env_checker:
      for console in configuration.console_manager:
        if console.is_enabled():
          # Consoles assume they have a ROMs directory
          env_checker.require_directory_exists(configuration.roms_directory_for_console(console))
    self.validated_configuration = True

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
      env_checker.require_writable_path(user.grid_directory())

  def main(self, dry_run=False):
    self.logger.info("=========== Starting Ice ===========")
    try:
      self.validate_base_environment()
      self.validate_configuration(self.config)
    except EnvCheckerError as e:
      self.logger.info("Ice cannot run because of issues with your system.\n")
      self.logger.info("* %s" % e.message)
      self.logger.info("\nPlease resolve these issues and try running Ice again")
      return
    # TODO: Create any missing directories that Ice will need
    self.logger.log_configuration(self.config)
    for user in self.users:
      self.logger.info("=========== User: %s ===========" % str(user.id32))
      self.run_for_user(user, dry_run=dry_run)

  def run_for_user(self, user, dry_run=False):
    try:
      self.validate_base_environment()
      self.validate_configuration(self.config)
      self.validate_user_environment(user)
    except EnvCheckerError as e:
      self.logger.info("Ice cannot run because of issues with your system.\n")
      self.logger.info("\t%s\n" % e.message)
      self.logger.info("Please resolve these issues and try running Ice again")
      return
    if not dry_run:
      self.logger.debug("Not creating backup because its a dry run")
      backup_path = self.config.shortcuts_backup_path(user)
      user.save_shortcuts(backup_path)
    # Find all of the ROMs that are currently in the designated folders
    roms = self.rom_finder.roms_for_consoles(self.config.console_manager)
    self.shortcut_synchronizer.sync_roms_for_user(user, roms, self.config, dry_run=dry_run)
    self.grid_updater.update_artwork_for_rom_collection(user, roms, dry_run=dry_run)

  def run(self, dry_run=False):
    try:
      self.main(dry_run=dry_run)
    except Exception as error:
      self.logger.exception("An exception occurred while running Ice")
