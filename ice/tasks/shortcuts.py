#!/usr/bin/env python
# encoding: utf-8

from ice import backups
from ice import history
from ice import paths
from ice.logs import logger
from ice.steam_shortcut_synchronizer import SteamShortcutSynchronizer

class SyncShortcutsTask(object):

  def __init__(self, app_settings):
    self.app_settings = app_settings

    managed_rom_archive = history.ManagedROMArchive(paths.archive_path())
    self.shortcut_synchronizer = SteamShortcutSynchronizer(app_settings.config, managed_rom_archive)

  def __call__(self, users, roms, dry_run):
    for user in users:
      logger.info("=========== User: %s ===========" % str(user.user_id))
      if dry_run:
        logger.debug("Not creating backup because its a dry run")
      else:
        logger.info("::Backing up shortcuts")
        backups.create_backup_of_shortcuts(self.app_settings.config, user)

      logger.info("::Syncing Shortcuts")
      self.shortcut_synchronizer.sync_roms_for_user(user, roms, self.app_settings.consoles, dry_run=dry_run)
