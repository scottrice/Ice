
from ice.emulator import Emulator

class EmulatorBackedObjectAdapter(object):

  def new(self, backing_store, identifier):
    return Emulator(backing_store, identifier)

  def save_in_store(self, backing_store, identifier, emulator):
    backing_store.set(identifier, 'location', emulator.location)
    backing_store.set(identifier, 'command', emulator.format)
