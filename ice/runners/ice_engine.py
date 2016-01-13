"""
IceEngine

The job of this class is to perform the functionality that Ice is defined by.
By that I mean the high level goal of `Adding ROMs to Steam`.
"""

import os

from pysteam import paths as steam_paths
from pysteam import shortcuts
from pysteam import steam

from ice import backups
from ice import consoles
from ice import emulators
from ice import paths
from ice.configuration import Configuration
from ice.error.env_checker_error import EnvCheckerError
from ice.environment_checker import EnvironmentChecker
from ice.gridproviders.combined_provider import CombinedProvider
from ice.gridproviders.consolegrid_provider import ConsoleGridProvider
from ice.gridproviders.local_provider import LocalProvider
from ice.history.managed_rom_archive import ManagedROMArchive
from ice.logs import logger
from ice.parsing.rom_parser import ROMParser
from ice.persistence.config_file_backing_store import ConfigFileBackingStore
from ice.rom_finder import ROMFinder
from ice.steam_grid_updater import SteamGridUpdater
from ice.steam_shortcut_synchronizer import SteamShortcutSynchronizer

def _path_with_override(filesystem, path_override, default_name):
  if path_override is not None:
    return path_override
  return paths.highest_precedent_data_file(filesystem, default_name)

class IceEngine(object):

  def __init__(self, steam, filesystem, options):
    """Valid options for creating an IceEngine are as follows:

    * config    - The path to the config file to use. Searches the default paths
                  for 'config.txt' otherwise
    * consoles  - The path to the consoles file to use. Searches the default
                  paths for 'consoles.txt' if none is provided
    * emulators - The path to the emulators file to use. Searches the default
                  paths for 'emulators.txt' if none is provided
    """
    self.validated_base_environment = False
    self.validated_configuration = False
    self.filesystem = filesystem
    logger.debug("Initializing Ice")
    config_data_path = _path_with_override(filesystem, options.config, "config.txt")
    consoles_data_path = _path_with_override(filesystem, options.consoles, "consoles.txt")
    emulators_data_path = _path_with_override(filesystem, options.emulators, "emulators.txt")
    self.config = Configuration(
        ConfigFileBackingStore(config_data_path),
        ConfigFileBackingStore(consoles_data_path),
        ConfigFileBackingStore(emulators_data_path),
        filesystem,
    )
    self.steam = steam

    parser = ROMParser()
    self.rom_finder = ROMFinder(self.config, filesystem, parser)
    archive_data_path = paths.highest_precedent_data_file(filesystem, "archive.json")
    managed_rom_archive = ManagedROMArchive(archive_data_path)
    self.shortcut_synchronizer = SteamShortcutSynchronizer(managed_rom_archive)

    provider = CombinedProvider(
        LocalProvider(),
        ConsoleGridProvider(),
    )
    self.grid_updater = SteamGridUpdater(provider)

  def validate_base_environment(self):
    """
    Validate that the current environment meets all of Ice's requirements.
    """
    if self.validated_base_environment:
      return
    with EnvironmentChecker(self.filesystem) as env_checker:
      # If Steam is running then any changes we make will be overwritten
      env_checker.require_program_not_running("Steam")
      # I'm not sure if there are situations where this won't exist, but I
      # assume that it does everywhere and better safe than sorry
      env_checker.require_directory_exists(self.steam.userdata_directory)
      # This is used to store history information and such
      env_checker.require_directory_exists(paths.application_data_directory())
    self.validated_base_environment = True

  def validate_configuration(self, configuration):
    if self.validated_configuration:
      return
    with EnvironmentChecker(self.filesystem) as env_checker:
      for console in configuration.console_manager:
        if consoles.console_is_enabled(console):
          # Consoles assume they have a ROMs directory
          env_checker.require_directory_exists(consoles.console_roms_directory(configuration, console))
    self.validated_configuration = True

  def validate_user_environment(self, user):
    """
    Validate that the current environment for a given user meets all of
    Ice's requirements.
    """
    with EnvironmentChecker(self.filesystem) as env_checker:
      # If the user hasn't added any grid images on their own then this
      # directory wont exist, so we require it explicitly here
      env_checker.require_directory_exists(steam_paths.custom_images_directory(user))
      # And it needs to be writable if we are going to save images there
      env_checker.require_writable_path(steam_paths.custom_images_directory(user))

  def main(self, dry_run=False):
    if self.steam is None:
      logger.error("Cannot run Ice because Steam doesn't appear to be installed")
      return

    logger.info("=========== Starting Ice ===========")
    try:
      self.validate_base_environment()
      self.validate_configuration(self.config)
    except EnvCheckerError as e:
      logger.info("Ice cannot run because of issues with your system.\n")
      logger.info("* %s" % e.message)
      logger.info("\nPlease resolve these issues and try running Ice again")
      return
    # TODO: Create any missing directories that Ice will need
    log_configuration(self.config)
    for user_context in steam.local_user_contexts(self.steam):
      logger.info("=========== User: %s ===========" % str(user_context.user_id))
      self.run_for_user(user_context, dry_run=dry_run)

  def run_for_user(self, user, dry_run=False):
    try:
      self.validate_base_environment()
      self.validate_configuration(self.config)
      self.validate_user_environment(user)
    except EnvCheckerError as e:
      logger.info("Ice cannot run because of issues with your system.\n")
      logger.info("\t%s\n" % e.message)
      logger.info("Please resolve these issues and try running Ice again")
      return
    if dry_run:
      logger.debug("Not creating backup because its a dry run")
    else:
      backups.create_backup_of_shortcuts(self.config, user)
    # Find all of the ROMs that are currently in the designated folders
    roms = self.rom_finder.roms_for_consoles(self.config.console_manager)
    self.shortcut_synchronizer.sync_roms_for_user(user, roms, self.config, dry_run=dry_run)
    self.grid_updater.update_artwork_for_rom_collection(user, roms, dry_run=dry_run)

  def run(self, dry_run=False):
    try:
      self.main(dry_run=dry_run)
    except Exception as error:
      logger.exception("An exception occurred while running Ice")

# Logging methods. The purpose of these methods isn't so much to log things as
# they are to inform the user of the state of their setup (as Ice sees it).
# They were originally on ice_logging but since they require knowledge of
# emulators/consoles/configurations it meant that I couldn't log from a bunch
# of different files. Clearly not ideal, and they weren't exactly a great fit
# on the logger class anyway
#
# TODO(scottrice): Find a better home for these functions

def log_emulator_state(emulator):
  if emulators.emulator_is_enabled(emulator):
    logger.info("Detected Emulator: %s" % emulator.name)
  else:
    logger.warning("Issue detected with emulator `%s`" % emulator.name)

def log_console_state(console):
  """
  Logs whether a console is enabled or not.
  """
  if consoles.console_is_enabled(console):
    logger.info("Detected Console: %s => %s" % (console.fullname, console.emulator.name))
  # TODO: Move this logic into a function on Console which gives a
  # stringified reason why the console is not enabled
  elif console.emulator is None:
    logger.warning("No emulator provided for console `%s`" % console.fullname)
  else:
    logger.warning("Issue detected with console `%s`" % console.fullname)

def log_configuration(config):
  logger.debug("Using `config.txt` at `%s`" % config.config_backing_store.path)
  logger.debug(
      "Using `consoles.txt` at `%s`" %
      config.console_manager.backing_store.path)
  logger.debug(
      "Using `emulators.txt` at `%s`" %
      config.emulator_manager.backing_store.path)
  for emulator in config.emulator_manager:
    log_emulator_state(emulator)
  for console in config.console_manager:
    log_console_state(console)
