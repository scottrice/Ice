
from functools import partial

import consoles

from rom import ROM

class ROMFinder(object):

  def __init__(self, config, filesystem, parser):
    self.config     = config
    self.filesystem = filesystem
    self.parser = parser

  def rom_for_path(self, console, path):
    name = self.parser.parse(path)
    return ROM(path, console, name)

  def roms_for_console(self, console):
    """
    @param console - A console object
    @returns A list of ROM objects representing all of the valid ROMs for a
             given console.

    Valid ROMs are defined as ROMs for which the function `path_is_rom` returns
    True when given the console.

    Returns an empty list if `console` is not enabled
    """
    if not consoles.console_is_enabled(console):
      return []

    roms_directory = self.config.roms_directory_for_console(console)
    paths = self.filesystem.files_in_directory(roms_directory, include_subdirectories=True)
    valid_rom_paths = filter(partial(consoles.path_is_rom, console), paths)
    return map(partial(self.rom_for_path, console), valid_rom_paths)

  def roms_for_consoles(self, consoles):
    """
    @param consoles - An iterable list of consoles
    @returns A list of all of the ROMs for all of the consoles in `consoles`

    Equivalent to calling `roms_for_console` on every element of `consoles`
    and combining the results
    """
    # Abuses the fact that the `+` operator is overloaded with lists to turn
    # our list of lists into a single giant list. Yay for duck typing?
    return sum(map(self.roms_for_console, consoles), [])
