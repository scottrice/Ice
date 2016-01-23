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
from ice import settings
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
    self.validated_consoles = False

    self.steam = steam
    self.filesystem = filesystem

    logger.debug("Initializing Ice")
    self.config    = settings.load_configuration(filesystem, options.config)
    self.emulators = settings.load_emulators(filesystem, options.emulators)
    self.consoles  = settings.load_consoles(self.emulators, filesystem, options.consoles)

    parser = ROMParser()
    self.rom_finder = ROMFinder(self.config, filesystem, parser)
    managed_rom_archive = ManagedROMArchive(paths.archive_path())
    self.shortcut_synchronizer = SteamShortcutSynchronizer(self.config, managed_rom_archive)

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

  def validate_consoles(self):
    if self.validated_consoles:
      return
    with EnvironmentChecker(self.filesystem) as env_checker:
      for console in self.consoles:
        # Consoles assume they have a ROMs directory
        env_checker.require_directory_exists(consoles.console_roms_directory(self.config, console))
    self.validated_consoles = True

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
      self.validate_consoles()
    except EnvCheckerError as e:
      logger.info("Ice cannot run because of issues with your system.\n")
      logger.info("* %s" % e.message)
      logger.info("\nPlease resolve these issues and try running Ice again")
      return

    # TODO: Create any missing directories that Ice will need
    log_emulators(self.emulators)
    log_consoles(self.consoles)

    for user_context in steam.local_user_contexts(self.steam):
      if user_context.user_id == "anonymous":
        continue
      logger.info("=========== User: %s ===========" % str(user_context.user_id))
      self.run_for_user(user_context, dry_run=dry_run)

  def run_for_user(self, user, dry_run=False):
    try:
      self.validate_base_environment()
      self.validate_consoles()
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
    roms = self.rom_finder.roms_for_consoles(self.consoles)
    self.shortcut_synchronizer.sync_roms_for_user(user, roms, self.consoles, dry_run=dry_run)
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

def log_emulators(emulators):
  for emulator in emulators:
    logger.info("Detected Emulator: %s" % emulator.name)

def log_consoles(consoles):
  for console in consoles:
    logger.info("Detected Console: %s => %s" % (console.fullname, console.emulator.name))
