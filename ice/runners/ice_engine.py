"""
IceEngine

The job of this class is to perform the functionality that Ice is defined by.
By that I mean the high level goal of `Adding ROMs to Steam`.
"""

import os

from pysteam import paths as steam_paths
from pysteam import shortcuts
from pysteam import steam as steam_module

from ice import backups
from ice import configuration
from ice import consoles
from ice import decorators
from ice import emulators
from ice import paths
from ice import settings
from ice.error.env_checker_error import EnvCheckerError
from ice.environment_checker import EnvironmentChecker
from ice.history.managed_rom_archive import ManagedROMArchive
from ice.logs import logger
from ice.parsing.rom_parser import ROMParser
from ice.persistence.config_file_backing_store import ConfigFileBackingStore
from ice.rom_finder import ROMFinder
from ice.steam_grid_updater import SteamGridUpdater
from ice.steam_shortcut_synchronizer import SteamShortcutSynchronizer

STEAM_CHECK_SKIPPED_WARNING = """\
Not checking whether Steam is running. Any changes made may be overwritten \
when Steam exits.\
"""

class IceEngine(object):

  def __init__(
    self,
    steam,
    filesystem,
    file_overrides):
    """Valid options for creating an IceEngine are as follows:

    * config    - The path to the config file to use. Searches the default paths
                  for 'config.txt' otherwise
    * consoles  - The path to the consoles file to use. Searches the default
                  paths for 'consoles.txt' if none is provided
    * emulators - The path to the emulators file to use. Searches the default
                  paths for 'emulators.txt' if none is provided
    """
    self.steam = steam
    self.filesystem = filesystem

    # We want to ignore the anonymous context, cause theres no reason to sync
    # ROMs for it since you cant log in as said user.
    is_user_context = lambda context: context.user_id != 'anonymous'
    self.users = filter(is_user_context, steam_module.local_user_contexts(self.steam))

    logger.debug("Initializing Ice")
    self.config    = settings.load_configuration(filesystem, file_overrides['config'])
    self.emulators = settings.load_emulators(filesystem, file_overrides['emulators'])
    self.consoles  = settings.load_consoles(self.emulators, filesystem, file_overrides['consoles'])

    parser = ROMParser()
    self.rom_finder = ROMFinder(self.config, filesystem, parser)

    managed_rom_archive = ManagedROMArchive(paths.archive_path())
    self.shortcut_synchronizer = SteamShortcutSynchronizer(self.config, managed_rom_archive)

    self.grid_updater = SteamGridUpdater(settings.image_provider(self.config))

  def validate_environment(self, skip_steam_check):
    """
    Validate that the current environment meets all of Ice's requirements.
    """
    with EnvironmentChecker(self.filesystem) as env_checker:
      if not skip_steam_check:
        # If Steam is running then any changes we make will be overwritten
        env_checker.require_program_not_running("Steam")
      else:
        logger.warning(STEAM_CHECK_SKIPPED_WARNING)
      # I'm not sure if there are situations where this won't exist, but I
      # assume that it does everywhere and better safe than sorry
      env_checker.require_directory_exists(self.steam.userdata_directory)
      # This is used to store history information and such
      env_checker.require_directory_exists(paths.application_data_directory())

      for console in self.consoles:
        # Consoles assume they have a ROMs directory
        env_checker.require_directory_exists(consoles.console_roms_directory(self.config, console))

      for user in self.users:
        # If the user hasn't added any grid images on their own then this
        # directory wont exist, so we require it explicitly here
        env_checker.require_directory_exists(steam_paths.custom_images_directory(user))
        # And it needs to be writable if we are going to save images there
        env_checker.require_writable_path(steam_paths.custom_images_directory(user))

  def create_backup(self, user, dry_run=False):
    if dry_run:
      logger.debug("Not creating backup because its a dry run")
    else:
      backups.create_backup_of_shortcuts(self.config, user)

  @decorators.catch_exceptions("An exception occurred while running Ice")
  def run(
    self,
    skip_steam_check=False,
    dry_run=False):
    if self.steam is None:
      logger.error("Cannot run Ice because Steam doesn't appear to be installed")
      return

    logger.info("=========== Starting Ice ===========")
    try:
      self.validate_environment(skip_steam_check)
    except EnvCheckerError as e:
      logger.info("Ice cannot run because of issues with your system.\n")
      logger.info("* %s" % e.message)
      logger.info("\nPlease resolve these issues and try running Ice again")
      return

    # TODO: Create any missing directories that Ice will need
    log_emulators(self.emulators)
    log_consoles(self.consoles)

    roms = self.rom_finder.roms_for_consoles(self.consoles)
    for user in self.users:
      logger.info("=========== User: %s ===========" % str(user.user_id))
      self.create_backup(user, dry_run=dry_run)
      self.shortcut_synchronizer.sync_roms_for_user(user, roms, self.consoles, dry_run=dry_run)
      self.grid_updater.update_artwork_for_rom_collection(user, roms, dry_run=dry_run)

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
