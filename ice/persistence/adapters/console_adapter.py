
import os

from ice.logs import logger
from ice import model

class ConsoleBackedObjectAdapter(object):

  def __init__(self, emulators):
    self.emulators = emulators

  def new(self, backing_store, identifier):
    fullname              = identifier
    shortname             = backing_store.get(identifier, 'nickname', fullname)
    extensions            = backing_store.get(identifier, 'extensions', "")
    custom_roms_directory = backing_store.get(identifier, 'roms directory', "")
    prefix                = backing_store.get(identifier, 'prefix', "")
    icon                  = backing_store.get(identifier, 'icon', "")
    images_directory      = backing_store.get(identifier, 'images directory', "")
    emulator_identifier   = backing_store.get(identifier, 'emulator', "")

    icon = os.path.expanduser(icon)
    custom_roms_directory = os.path.expanduser(custom_roms_directory)
    images_directory = os.path.expanduser(images_directory)

    emulator = self.emulators.find(emulator_identifier)

    return model.Console(
      fullname,
      shortname,
      extensions,
      custom_roms_directory,
      prefix,
      icon,
      images_directory,
      emulator,
    )

  def verify(self, console):
    if console.emulator is None:
      logger.debug("No emulator provided for console `%s`" % console.fullname)
      return False

    return True

  def save_in_store(self, backing_store, identifier, console):
    backing_store.set(identifier, 'nickname', console.shortname)
    backing_store.set(identifier, 'extensions', console.extensions)
    backing_store.set(identifier, 'roms directory', console.custom_roms_directory)
    backing_store.set(identifier, 'prefix', console.prefix)
    backing_store.set(identifier, 'icon', console.icon)
    backing_store.set(identifier, 'images directory', console.images_directory)
    backing_store.set(identifier, 'emulator', console.emulator.name)
