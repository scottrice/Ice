"""
console_manager.py

Created by Scott on 2014-08-20.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from backed_object_manager import BackedObjectManager
from ice.console import Console


class ConsoleManager(BackedObjectManager):

  def __init__(self, backing_store, config):
    super(ConsoleManager, self).__init__(backing_store)
    self.config = config

  def new(self, identifier):
    return Console(self.backing_store, identifier, self.config)
