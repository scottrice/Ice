#!/usr/bin/env python
# encoding: utf-8
"""
settings.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

Basic settings to be used by the app.
"""

import ConfigParser
import os

from configuration import Configuration
from persistence.config_file_backing_store import ConfigFileBackingStore
import utils

def __in_app_data_or_local(filename):
  app_data_path = os.path.join(utils.app_data_directory(), filename)
  if os.path.isfile(app_data_path):
    return app_data_path
  else:
    return os.path.abspath(filename)

def user_settings_path():
  return __in_app_data_or_local("config.txt")

def user_consoles_path():
  return __in_app_data_or_local("consoles.txt")

def user_emulators_path():
  return __in_app_data_or_local("emulators.txt")

config = Configuration(user_settings_path())

def _config_file_to_dictionary(path):
  config = ConfigParser.ConfigParser()
  config.read(path)
  settings = {}
  for section in config.sections():
    settings[section] = {}
    for option in config.options(section):
      settings[section][option] = config.get(section,option)
  return settings

def settings_for_file(file):
  return {
    "config.txt": config(),
    "consoles.txt": consoles(),
    "emulators.txt": emulators(),
  }[file]