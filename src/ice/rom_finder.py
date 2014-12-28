
from console import Console
from rom import ROM

class ROMFinder(object):
  def __init__(self, filesystem):
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

    paths = self.filesystem.files_in_directory(console.roms_directory())
    valid_rom_paths = filter(console.is_valid_rom, paths)
    return map(lambda path: ROM(path, console), valid_rom_paths)

  def roms_for_consoles(self, consoles):
    """
    @param consoles - An iterable list of consoles
    @returns A list of all of the ROMs for all of the consoles in `consoles`

    Equivalent to calling `roms_for_console` on every element of `consoles` 
    and combining the results
    """
    assert hasattr(consoles, '__iter__'), "Expecting an iterable list of consoles"
    def rom_collector(roms, console):
      roms.extend(self.roms_for_console(console))
      return roms
    return reduce(rom_collector, consoles, [])