
import os

from ice.logs import logger
from ice.model import Emulator

class EmulatorBackedObjectAdapter(object):

  def __init__(self, filesystem):
    self.filesystem = filesystem

  def new(self, backing_store, identifier):
    name     = identifier
    location = backing_store.get(identifier, 'location')
    fmt      = backing_store.get(identifier, 'command', "%l %r")

    location = os.path.expanduser(location)

    return Emulator(
      name,
      location,
      fmt,
    )

  def verify(self, emulator):
    if emulator.location is None or emulator.location == "":
      logger.error("Missing location for Emulator: `%s`" % emulator.name)
      return False

    if not self.filesystem.is_file(emulator.location):
      logger.error("Could not find a file at `%s`, which is set as the " \
                   "location for `%s`." % (emulator.location, emulator.name))
      logger.error("Launching your game in Steam might not work.")
      # It seems like we would return False here, but since this is a common
      # source of confusion, if people want to shoot themselves in the foot we
      # should let them. Just make sure they know they're doing it.

    return True

  def save_in_store(self, backing_store, identifier, emulator):
    assert(identifier == emulator.name)
    backing_store.set(identifier, 'location', emulator.location)
    backing_store.set(identifier, 'command', emulator.format)
