# encoding: utf-8
"""
config_file_backing_store.py

Created by Scott on 2014-08-12.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import ConfigParser

import backing_store

class ConfigFileBackingStore(backing_store.BackingStore):

  def __init__(self, filename):
    self.configParser = ConfigParser.RawConfigParser()
    self.path = filename

    self.configParser.read(self.path)

  def identifiers(self):
    self.configParser.sections()

  def add_identifier(self, ident):
    try:
      self.configParser.add_section(ident)
    except ConfigParser.DuplicateSectionError:
      raise ValueError("A section with the id `%s` already exists" % str(id))

  def remove_identifier(self, ident):
    try:
      self.configParser.remove_section(ident)
    except ConfigParser.NoSectionError:
      raise ValueError("Cannot remove a section with the id `%s` because none exists" % str(id))

  def keys(self, ident):
    return self.configParser.options(ident)

  def get(self, ident, key, default=None):
    return self.configParser.get(ident, key.lower())

  def set(self, ident, key, value):
    self.configParser.set(ident, key.lower(), value)

  def save(self):
    try:
      with open(self.path, "w") as configFile:
        self.configParser.write(configFile)
    except IOError:
      raise IOError("Cannot save data to `%s`. Permission Denied")
