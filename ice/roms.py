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

from pysteam import model

import emulators
import paths

# LEGACY: At one point I added this to every shortcut that Ice made. That was
# a terrible idea, and I'm keeping this definition here just in case I ever
# have to clean up after myself
ICE_FLAG_TAG = "~ManagedByIce"

def roms_directory(config):
  user_override = config.roms_directory
  if user_override is not None:
    return user_override
  return paths.default_roms_directory()

def rom_shortcut_name(rom):
  """Calculates what a ROM's name should be when represented as a shortcut in
  Steam. For the most part this is just the name of the ROM itself, but some
  Console's provide a prefix which should be appended to the name of the ROM
  itself."""
  prefix = rom.console.prefix
  if prefix:
    return "%s %s" % (prefix, rom.name)
  else:
    return rom.name

def rom_to_shortcut(rom):
  emu = rom.console.emulator
  assert(emu is not None)

  return model.Shortcut(
    name      = rom_shortcut_name(rom),
    exe       = emulators.emulator_rom_launch_command(emu, rom),
    startdir  = emulators.emulator_startdir(emu),
    icon      = rom.console.icon,
    tags      = [rom.console.fullname]
  )
