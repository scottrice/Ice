#!/usr/bin/env python
# encoding: utf-8
"""
settings.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

Basic settings to be used by the app.
"""

import sys
import os
import ConfigParser

appname = "Ice"
appdescription = "ROM Manager for Steam"
appauthor = "Scott Rice"

config_dict = None
consoles_dict = None
emulators_dict = None

def user_settings_path():
  return "config.txt"

def user_consoles_path():
  return "consoles.txt"

def user_emulators_path():
  return "emulators.txt"

def _config_file_to_dictionary(path):
  config = ConfigParser.ConfigParser()
  config.read(path)
  settings = {}
  for section in config.sections():
    settings[section] = {}
    for option in config.options(section):
      settings[section][option] = config.get(section,option)
  return settings

def config():
  global config_dict
  if config_dict == None:
    config_dict = _config_file_to_dictionary(user_settings_path())
  return config_dict

def consoles():
  global consoles_dict
  if consoles_dict == None:
    consoles_dict = _config_file_to_dictionary(user_consoles_path())
  return consoles_dict

def emulators():
  global emulators_dict
  if emulators_dict == None:
    emulators_dict = _config_file_to_dictionary(user_emulators_path())
  return emulators_dict

def settings_for_file(file):
  return {
    "config.txt": config(),
    "consoles.txt": consoles(),
    "emulators.txt": emulators(),
  }[file]