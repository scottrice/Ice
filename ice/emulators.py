# encoding: utf-8

import os

def emulator_rom_launch_command(emulator, rom):
  """Generates a command string that will launch `rom` with `emulator` (using
  the format provided by the user). The return value of this function should
  be suitable to use as the `Exe` field of a Steam shortcut"""
  # Normalizing the strings is just removing any leading/trailing quotes.
  # The beautiful thing is that strip does nothing if it doesnt contain quotes,
  # so normalizing it then adding quotes should do what I want 100% of the time
  normalize = lambda s: s.strip("\"")
  add_quotes = lambda s: "\"%s\"" % s

  # We don't know if the user put quotes around the emulator location. If
  # so, we dont want to add another pair and screw things up.
  #
  # The user didnt give us the ROM information, but screw it, I already
  # have some code to add quotes to a string, might as well use it.
  quoted_location = add_quotes(normalize(emulator.location))
  quoted_rom      = add_quotes(normalize(rom.path))
  # The format string contains a bunch of specifies that users can use to
  # substitute values in at runtime. Right now the only supported values are:
  # %l - The location of the emulator (to avoid sync bugs)
  # %r - The location of the ROM (so the emulator knows what to launch)
  # %fn - The ROM filename without its extension (for emulators that utilize separete configuration files)
  #
  # More may be added in the future, but for now this is what we support
  return (
    emulator.format
      .replace("%l", quoted_location)
      .replace("%r", quoted_rom)
      .replace("%fn", os.path.splitext(os.path.basename(rom.path))[0])
  )

def emulator_startdir(emulator):
  """Returns the directory which stores the emulator. The return value of this
  function should be suitable to use as the 'StartDir' field of a Steam
  shortcut"""
  return os.path.dirname(emulator.location)
