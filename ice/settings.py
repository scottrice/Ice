#!/usr/bin/env python
# encoding: utf-8
"""
settings.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

Basic settings to be used by the app.
"""

import ConfigParser
import utils

from persistence.config_file_backing_store import ConfigFileBackingStore
from configuration import Configuration

def user_settings_path():
  return "config.txt"

def user_consoles_path():
  return "consoles.txt"

def user_emulators_path():
  return "emulators.txt"

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