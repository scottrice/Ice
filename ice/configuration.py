# encoding: utf-8
"""
configuration.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.

Wrapper class around the options that a user could set to configure Ice
"""

import collections
import os

import model
import paths

ConfigOption = collections.namedtuple('ConfigOption', [
  'identifier',
  'key',
  'default',
])

ROMsDirectoryOption = ConfigOption(
  identifier = "Storage",
  key = "ROMs Directory",
  default = None,
)

BackupDirectoryOption = ConfigOption(
  identifier = "Storage",
  key = "Backup Directory",
  default = None,
)

UserdataDirectoryOption = ConfigOption(
  identifier = "Steam",
  key = "Userdata Directory",
  default = None,
)

ProviderSpecOption = ConfigOption(
  identifier = "Images",
  key = "Providers",
  default = "local, consolegrid",
)

def get(store, option):
  return store.get(option.identifier, option.key, option.default)

def get_directory(store, option):
  path = get(store, option)
  if path is not None:
    path = os.path.expanduser(path)
  return path

def from_store(store):
  """Builds a Configuration object (defined in the model)"""
  return model.Configuration(
    backup_directory = get_directory(store, BackupDirectoryOption),
    provider_spec = get(store, ProviderSpecOption),
    roms_directory = get_directory(store, ROMsDirectoryOption),
    userdata_directory = get_directory(store, UserdataDirectoryOption),
  )
