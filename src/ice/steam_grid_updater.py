class SteamGridUpdater(object):

  def __init__(self, provider, logger):
    self.provider = provider
    self.logger = logger

  def update_rom_artwork(self, user, rom, dry_run=False):
    shortcut = rom.to_shortcut()
    if shortcut.custom_image(user) is not None:
      # If the user already has a custom image for their game, dont override it
      return

    path = self.provider.image_for_rom(rom)

    if path is None:
      self.logger.info("No image found for `%s`" % shortcut.name)
      return

    if dry_run:
      self.logger.debug("Found image, but not setting because its a dry run")
      return

    self.logger.info("Found grid image for `%s`" % shortcut.name)
    shortcut.set_image(user, path)

  def update_artwork_for_rom_collection(self, user, roms, dry_run=False):
    map(lambda rom: self.update_rom_artwork(user, rom, dry_run=dry_run), roms)
