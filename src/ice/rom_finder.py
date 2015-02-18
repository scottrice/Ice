
from ice.console import Console
from ice.rom import ROM
from functools import reduce


class ROMFinder(object):

  def __init__(self, config, filesystem):
    self.config     = config
    self.filesystem = filesystem

  def roms_for_console(self, console):
    """
    @param console - A console object
    @returns A list of ROM objects representing all of the valid ROMs for a
             given console.

    Valid ROMs are defined as ROMs for which `console`'s `is_valid_rom` method
    returns True.

    Returns an empty list if `console` is not enabled
    """
    if not console.is_enabled():
      return []

    roms_directory = self.config.roms_directory_for_console(console)
    paths = self.filesystem.files_in_directory(roms_directory)
    valid_rom_paths = filter(console.is_valid_rom, paths)
    return list(map(lambda path: ROM(path, console), valid_rom_paths))

  def roms_for_consoles(self, consoles):
    """
    @param consoles - An iterable list of consoles
    @returns A list of all of the ROMs for all of the consoles in `consoles`

    Equivalent to calling `roms_for_console` on every element of `consoles`
    and combining the results
    """
    return reduce(lambda roms, console: roms + self.roms_for_console(console), consoles, [])
