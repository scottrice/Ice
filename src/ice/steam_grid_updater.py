
from error import provider_error

class SteamGridUpdater(object):
  def __init__(self, provider, logger):
    self.provider = provider
    self.logger = logger

  def update_rom_artwork(self, user, rom):
    shortcut = rom.to_shortcut()
    if shortcut.custom_image(user) is not None:
      # If the user already has a custom image for their game, dont override it
      return

    try:
      path = self.provider.image_for_rom(rom)
    except provider_error.ProviderError as error:
      self.logger.debug(error)
      path = None

    if path:
      self.logger.info("Found grid image for `%s`" % shortcut.name)
      shortcut.set_image(user, path)
    else:
      self.logger.info("No image found for `%s`" % shortcut.name)

  def update_artwork_for_rom_collection(self, user, roms):
    map(lambda rom: self.update_rom_artwork(user, rom), roms)
