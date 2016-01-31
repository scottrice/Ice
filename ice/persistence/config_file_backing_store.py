# encoding: utf-8
"""
config_file_backing_store.py

Created by Scott on 2014-08-12.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

# Python 2 and 3 compatibility for ConfigParser
try:
  from configparser import ConfigParser, RawConfigParser, NoSectionError, NoOptionError, DuplicateSectionError
except ImportError:
  from ConfigParser import ConfigParser, RawConfigParser, NoSectionError, NoOptionError, DuplicateSectionError

from . import backing_store


class ConfigFileBackingStore(backing_store.BackingStore):

  def __init__(self, path):
    super(ConfigFileBackingStore, self).__init__(path)
    self.configParser = RawConfigParser()
    self.configParser.read(self.path)

  def identifiers(self):
    return self.configParser.sections()

  def add_identifier(self, ident):
    try:
      self.configParser.add_section(ident)
    except DuplicateSectionError:
      raise ValueError("The identifier `%s` already exists" % str(ident))

  def remove_identifier(self, ident):
    self.configParser.remove_section(ident)

  def keys(self, ident):
    try:
      return self.configParser.options(ident)
    except NoSectionError:
      raise ValueError("No identifier named `%s` exists" % str(ident))

  def get(self, ident, key, default=None):
    try:
      val = self.configParser.get(ident, key.lower())
      return val
    except (NoSectionError, NoOptionError):
      return default

  def set(self, ident, key, value):
    self.configParser.set(ident, key.lower(), value)

  def save(self):
    try:
      with open(self.path, "w") as configFile:
        self.configParser.write(configFile)
    except IOError:
      raise IOError("Cannot save data to `%s`. Permission Denied")
