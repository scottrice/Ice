"""
emulator_manager.py

Created by Scott on 2014-08-20.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from backed_object_manager import BackedObjectManager
from ice.emulator import Emulator


class EmulatorManager(BackedObjectManager):

  def __init__(self, backing_store):
    super(EmulatorManager, self).__init__(backing_store)

  def new(self, identifier):
    return Emulator(self.backing_store, identifier)
