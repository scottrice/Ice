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

  def sections(self):
    self.configParser.sections()

  def add_section(self, id):
    try:
      self.configParser.add_section(id)
    except ConfigParser.DuplicateSectionError:
      raise ValueError("A section with the id `%s` already exists" % str(id))

  def remove_section(self, id):
    try:
      self.configParser.remove_section(id)
    except ConfigParser.NoSectionError:
      raise ValueError("Cannot remove a section with the id `%s` because none exists" % str(id))

  def keys(self, section):
    return self.configParser.options(section)

  def get(self, section, key):
    return self.configParser.get(section, key.lower())

  def set(self, section, key, value):
    self.configParser.set(section, key.lower(), value)

  def save(self):
    try:
      with open(self.path, "w") as configFile:
        self.configParser.write(configFile)
    except IOError:
      raise IOError("Cannot save data to `%s`. Permission Denied")
