#!/usr/bin/env python
# encoding: utf-8
"""
configuration.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.

Wrapper class around the options that a user could set to configure Ice
"""

import os
from datetime import datetime

from persistence.config_file_backing_store import ConfigFileBackingStore
from utils import app_data_directory as data_directory

class Configuration(object):

    def __init__(self, config_path):
      self.backing_store = ConfigFileBackingStore(config_path)

    def _get_directory_(self, identifier, key, default):
      # TODO: Clean up this function and write tests for the callsites
      path = self.backing_store.get(identifier, key, default)
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
      return self._get_directory_(
        'Storage',
        'ROMs Directory',
        os.path.join('~', 'ROMs')
      )

    def backup_directory(self):
      return self._get_directory_(
        'Storage',
        'Backup Directory',
        os.path.join(data_directory(), 'Backups')
      )

    def shortcuts_backup_path(self, user, timestamp_format="%Y%m%d%H%M%S"):
      """
      Returns the path for a shortcuts.vdf backup file.

      This path is in the designated backup directory, and includes a timestamp
      before the extension to allow many backups to exist at once.
      """
      timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
      filename = "shortcuts." + timestamp + ".vdf"
      return os.path.join(
          self.backup_directory(),
          str(user.id32),
          'config',
          filename
      )