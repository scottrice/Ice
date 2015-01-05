#!/usr/bin/env python
# encoding: utf-8
"""
console.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

This class represents the Console datatype. Each ROM is associated with a
Console, and each Console has many ROMs. A Console also is associated with an
emulator, which can be used to play a ROM.

Functionality should be added to this class/module if it deals with Consoles or
their emulators. This includes finding a list of ROMs in this console's folder.
"""

import os

import utils
from persistence.backed_object import BackedObject
from persistence.config_file_backing_store import ConfigFileBackingStore
from emulator import Emulator
from rom import ROM


class Console(BackedObject):

  def __init__(self, backing_store, identifier, config):
    super(Console, self).__init__(backing_store, identifier)
    self.config = config

    self.fullname = identifier
    self.shortname = self.backed_value('nickname', self.fullname)
    self.extensions = self.backed_value('extensions', "")
    self.custom_roms_directory = self.backed_value('roms directory', "")
    self.prefix = self.backed_value('prefix', "")
    self.icon = self.backed_value('icon', "")
    self.images_directory = self.backed_value('images directory', "")
    self.emulator_identifier = self.backed_value('emulator', "")

    self.icon = os.path.expanduser(self.icon)
    self.custom_roms_directory = os.path.expanduser(self.custom_roms_directory)
    self.images_directory = os.path.expanduser(self.images_directory)

    self.emulator = config.emulator_manager.find(self.emulator_identifier)

  def __repr__(self):
    return self.fullname

  def is_enabled(self):
    return self.emulator is not None

  def is_valid_rom(self, path):
    """
    This function determines if a given path is actually a valid ROM file.
    If a list of extensions is supplied for this console, we check if the path has a valid extension
    If no extensions are defined for this console, we just accept any file
    """

    if self.extensions == "":
      return True
    extension = os.path.splitext(path)[1].lower()
    return any(extension == ('.' + x.strip().lower())
               for x in self.extensions.split(','))
