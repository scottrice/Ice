
from ice.console import Console

class ConsoleBackedObjectAdapter(object):

  def __init__(self, emulators):
    self.emulators = emulators

  def new(self, backing_store, identifier):
    return Console(backing_store, identifier, self.emulators)
