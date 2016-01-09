
from pysteam import grid
from pysteam import shortcuts

import roms

from logs import logger

class SteamGridUpdater(object):

  def __init__(self, provider):
    self.provider = provider

  def update_rom_artwork(self, user, rom, dry_run=False):
    shortcut = roms.rom_to_shortcut(rom)
    logger.debug("Updating image for %s (%s)" % (rom, shortcut))
    app_id = shortcuts.shortcut_app_id(shortcut)

    if grid.has_custom_image(user, app_id):
      existing_image = grid.get_custom_image(user, app_id)
      logger.debug("Not looking for new images for %s, it already has a grid image (%s)" % (shortcut.name, existing_image))
      return

    path = self.provider.image_for_rom(rom)

    if path is None:
      logger.info("No image found for `%s`" % shortcut.name)
      return

    if dry_run:
      logger.debug("Found image, but not setting because its a dry run")
      return

    logger.info("Found grid image for `%s`" % shortcut.name)
    grid.set_custom_image(user, app_id, path)

  def update_artwork_for_rom_collection(self, user, roms, dry_run=False):
    map(lambda rom: self.update_rom_artwork(user, rom, dry_run=dry_run), roms)
