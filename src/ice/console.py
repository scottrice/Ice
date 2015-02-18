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

from ice.rom import ROM


class Console(object):

  def __init__(self, fullname, shortname, extensions, custom_roms_directory, prefix, icon, images_directory, emulator):
    self.fullname = fullname
    self.shortname = shortname
    self.extensions = extensions
    self.custom_roms_directory = custom_roms_directory
    self.prefix = prefix
    self.icon = icon
    self.images_directory = images_directory
    self.emulator = emulator

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
