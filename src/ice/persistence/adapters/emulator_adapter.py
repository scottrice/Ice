
from ice.emulator import Emulator

class EmulatorBackedObjectAdapter(object):

  def new(self, backing_store, identifier):
    return Emulator(backing_store, identifier)
