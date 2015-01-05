
from ice.console import Console

class ConsoleBackedObjectAdapter(object):

  def __init__(self, emulators):
    self.emulators = emulators

  def new(self, backing_store, identifier):
    return Console(backing_store, identifier, self.emulators)

  def save_in_store(self, backing_store, identifier, console):
    backing_store.set(identifier, 'nickname', console.shortname)
    backing_store.set(identifier, 'extensions', console.extensions)
    backing_store.set(identifier, 'roms directory', console.custom_roms_directory)
    backing_store.set(identifier, 'prefix', console.prefix)
    backing_store.set(identifier, 'icon', console.icon)
    backing_store.set(identifier, 'images directory', console.images_directory)
    backing_store.set(identifier, 'emulator', console.emulator.name)
