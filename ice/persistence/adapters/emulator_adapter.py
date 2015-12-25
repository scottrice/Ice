
import os

from ice.model import Emulator

class EmulatorBackedObjectAdapter(object):

  def __init__(self, logger, filesystem):
    self.logger = logger
    self.filesystem = filesystem

  def new(self, backing_store, identifier):
    name     = identifier
    location = backing_store.get(identifier, 'location')
    fmt      = backing_store.get(identifier, 'command', "%l %r")

    location = os.path.expanduser(location)

    if location is None:
      self.logger.error("Missing location for Emulator: `%s`" % name)

    if not self.filesystem.path_exists(location):
      self.logger.error("Could not find a file at `%s`, which is set as the location for `%s`." % (location, name))
      self.logger.error("Launching your game in Steam might not work.")

    return Emulator(
      name,
      location,
      fmt,
    )

  def save_in_store(self, backing_store, identifier, emulator):
    assert(identifier == emulator.name)
    backing_store.set(identifier, 'location', emulator.location)
    backing_store.set(identifier, 'command', emulator.format)
