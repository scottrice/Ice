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

import paths

from persistence.backed_object_manager import BackedObjectManager
from persistence.adapters.console_adapter import ConsoleBackedObjectAdapter
from persistence.adapters.emulator_adapter import EmulatorBackedObjectAdapter


class Configuration(object):

  ROM_IDENT = "Storage"
  ROM_KEY = "ROMs Directory"

  BACKUP_IDENT = "Storage"
  BACKUP_KEY = "Backup Directory"

  USERDATA_IDENT = "Steam"
  USERDATA_KEY = "Userdata Directory"

  def __init__(self, config_store, consoles_store, emulators_store, filesystem):
    self.config_backing_store = config_store
    self.consoles_backing_store = consoles_store
    self.emulators_backing_store = emulators_store
    self.emulator_manager = BackedObjectManager(
      emulators_store,
      EmulatorBackedObjectAdapter(filesystem)
    )
    self.console_manager = BackedObjectManager(
      consoles_store,
      ConsoleBackedObjectAdapter(self.emulator_manager)
    )

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
    return self._get_directory_from_store('Steam', 'Userdata Location', None)

  def roms_directory(self):
    return self._get_directory_from_store(
        self.ROM_IDENT,
        self.ROM_KEY,
        os.path.join('~', 'ROMs')
    )

  def set_roms_directory(self, dir):
    self.config_backing_store.set(
        self.ROM_IDENT,
        self.ROM_KEY,
        dir
    )
    self.config_backing_store.save()

  def backup_directory(self):
    return self._get_directory_from_store(
        self.BACKUP_IDENT,
        self.BACKUP_KEY,
        None
    )

  def set_backup_directory(self, dir):
    self.config_backing_store.set(
        self.BACKUP_IDENT,
        self.BACKUP_KEY,
        dir
    )
    self.config_backing_store.save()

  def userdata_directory(self):
    return self._get_directory_from_store(
        self.USERDATA_IDENT,
        self.USERDATA_KEY,
        os.path.join(paths.application_data_directory(), 'Userdata')
    )

  def set_userdata_directory(self, dir):
    self.config_backing_store.set(
        self.USERDATA_IDENT,
        self.USERDATA_KEY,
        dir
    )
    self.config_backing_store.save()
