#!/usr/bin/env python
# encoding: utf-8
"""
configuration.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.

Wrapper class around the options that a user could set to configure Ice
"""

import appdirs
import datetime
import os

from persistence.console_manager import ConsoleManager
from persistence.emulator_manager import EmulatorManager

class Configuration(object):

    @staticmethod
    def data_directory():
      # Parameters are 'App Name' and 'App Author'
      # TODO: Get these values from the same place as setup.py
      return appdirs.user_data_dir("Ice","Scott Rice")

    def __init__(self, config_store, consoles_store, emulators_store):
      self.config_backing_store = config_store
      self.consoles_backing_store = consoles_store
      self.emulators_backing_store = emulators_store
      self.console_manager = ConsoleManager(consoles_store, self)
      self.emulator_manager = EmulatorManager(emulators_store)
      # We initialize the emulators first so that when the consoles are
      # initialized they will be able to grab emulators using `find`
      self.emulator_manager.initialize()
      self.console_manager.initialize()

    def _get_directory_from_store(self, identifier, key, default):
      # TODO: Clean up this function and write tests for the callsites
      path = self.config_backing_store.get(identifier, key, default)
      if path is not None:
        return os.path.expanduser(path)
      elif default is not None:
        return os.path.expanduser(default)
      else:
        return default

    def steam_userdata_location(self):
      """
      Returns the user-supplied location of Steam's `userdata` directory.

      The defaults for each system aren't handled here, but instead inside
      pysteam. As such, this method will return None if the user hasn't
      specified a directory.
      """
      # We want to return None even if the empty string is given
      return self._directory_value_('Steam', 'Userdata Location', None)

    def roms_directory(self):
      return self._get_directory_from_store(
        'Storage',
        'ROMs Directory',
        os.path.join('~', 'ROMs')
      )

    def backup_directory(self):
      return self._get_directory_from_store(
        'Storage',
        'Backup Directory',
        os.path.join(Configuration.data_directory(), 'Backups')
      )

    def shortcuts_backup_path(self, user, timestamp_format="%Y%m%d%H%M%S"):
      """
      Returns the path for a shortcuts.vdf backup file.

      This path is in the designated backup directory, and includes a timestamp
      before the extension to allow many backups to exist at once.
      """
      timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
      filename = "shortcuts." + timestamp + ".vdf"
      return os.path.join(
          self.backup_directory(),
          str(user.id32),
          'config',
          filename
      )

    def valid_roms(self):
      """
      Returns all the `valid` ROMs. A ROM is considered valid if its console
      is enabled
      """
      valid_roms = []
      for console in self.console_manager:
        if console.is_enabled():
          valid_roms.extend(console.find_roms())
      return valid_roms
