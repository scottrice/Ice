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

  @staticmethod
  def data_directory():
    # Parameters are 'App Name' and 'App Author'
    # TODO: Get these values from the same place as setup.py
    return appdirs.user_data_dir("Ice", "Scott Rice")

  @staticmethod
  def path_for_data_file(filename):
    """
    Returns the path to a data file named `filename`.
    This function first checks to see if the data file exists in the data
    directory. If so, it returns that.
    Then, this function checks to see if the data file exists in the local
    directory. If so, it returns that.
    If neither of those things are true then this function will return the
    path to a new file in the data directory.
    """
    local_path = os.path.abspath(filename)
    data_path = os.path.join(Configuration.data_directory(), filename)
    if os.path.isfile(data_path):
      return data_path
    elif os.path.isfile(local_path):
      return local_path
    else:
      return data_path

  def __init__(self, config_store, consoles_store, emulators_store, logger, filesystem):
    self.config_backing_store = config_store
    self.consoles_backing_store = consoles_store
    self.emulators_backing_store = emulators_store
    self.emulator_manager = BackedObjectManager(
      emulators_store,
      EmulatorBackedObjectAdapter(logger, filesystem)
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

  def _has_backup_option_set(self):
    try:
      store = self.config_backing_store
      return self.BACKUP_KEY.lower() in store.keys(self.BACKUP_IDENT)
    except ValueError:
      # The backing store raises a ValueError if the identifier doesnt exist.
      # If the identifier doesnt exist, we clearly dont have this option set.
      return False

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
    if not self._has_backup_option_set():
      return None
    return self._get_directory_from_store(
        self.BACKUP_IDENT,
        self.BACKUP_KEY,
        os.path.join(Configuration.data_directory(), 'Backups')
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
        os.path.join(Configuration.data_directory(), 'Userdata')
    )

  def set_userdata_directory(self, dir):
    self.config_backing_store.set(
        self.USERDATA_IDENT,
        self.USERDATA_KEY,
        dir
    )
    self.config_backing_store.save()

  def shortcuts_backup_path(self, user, timestamp_format="%Y%m%d%H%M%S"):
    """
    Returns the path for a shortcuts.vdf backup file.

    This path is in the designated backup directory, and includes a timestamp
    before the extension to allow many backups to exist at once.
    """
    backup_dir = self.backup_directory()
    if backup_dir is None:
      return None

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = "shortcuts." + timestamp + ".vdf"
    return os.path.join(
        backup_dir,
        str(user.user_id),
        'config',
        filename
    )

  def roms_directory_for_console(self, console):
    """
    If the user has specified a custom ROMs directory in consoles.txt then
    return that.

    Otherwise, append the shortname of the console to the default ROMs
    directory given by config.txt.
    """
    if console.custom_roms_directory:
      return console.custom_roms_directory
    return os.path.join(self.roms_directory(), console.shortname)
