#!/usr/bin/env python
# encoding: utf-8

from ice import settings
from ice import steam_grid_updater
from ice.logs import logger

class UpdateGridImagesTask(object):

  def __init__(self, app_settings):
    provider = settings.image_provider(app_settings.config)
    self.grid_updater = steam_grid_updater.SteamGridUpdater(provider)

  def __call__(self, users, roms, dry_run):
    for user in users:
      logger.info("::Updating grid images for U:%s" % user.user_id)
      self.grid_updater.update_artwork_for_rom_collection(user, roms, dry_run=dry_run)
