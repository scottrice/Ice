#!/usr/bin/env python
# encoding: utf-8

from ice import settings
from ice import steam_grid_updater
from ice.logs import logger

class UpdateGridImagesTask(object):

  def __init__(self, rom_finder):
    self.rom_finder = rom_finder

  def __call__(self, app_settings, users, dry_run):
    roms = self.rom_finder.roms_for_consoles(
      app_settings.config,
      app_settings.consoles,
    )

    provider = settings.image_provider(app_settings.config)
    grid_updater = steam_grid_updater.SteamGridUpdater(provider)

    for user in users:
      logger.info("::Updating grid images for U:%s" % user.user_id)
      grid_updater.update_artwork_for_rom_collection(user, roms, dry_run=dry_run)
