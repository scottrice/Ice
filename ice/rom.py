# encoding: utf-8
"""
IceROM.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

ROM model. Handles the collection of data that makes up a ROM (as of right now,
just the path to the ROM and what console is is from). Also contains some
convenience methods for the filesystem.

Functionality should be added to this class if it heavily involves the use of
ROMs
"""

from pysteam.model import Shortcut

# LEGACY: At one point I added this to every shortcut that Ice made. That was
# a terrible idea, and I'm keeping this definition here just in case I ever
# have to clean up after myself
ICE_FLAG_TAG = "~ManagedByIce"


class ROM:

  def __init__(self, path, console, name):
    self.path = path
    self.console = console
    self.name = name

  def __repr__(self):
    return self.name

  def __eq__(self, other):
    return self.path == other.path and self.console == other.console

  def prefixed_name(self):
    prefix = self.console.prefix
    if prefix:
      return "%s %s" % (prefix, self.name())
    else:
      return self.name

  def to_shortcut(self):
    appname = self.prefixed_name()
    exe = self.console.emulator.command_string(self)
    startdir = self.console.emulator.startdir(self)
    icon = self.console.icon
    category = self.console.fullname
    tags = [category]
    return Shortcut(appname, exe, startdir, icon, tags)
