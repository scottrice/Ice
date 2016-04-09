
from functools import partial

import cache
import consoles
import model

from logs import logger

class ROMFinder(object):

  def __init__(self, filesystem, parser):
    self.filesystem   = filesystem
    self.parser       = parser

    self.search_cache = cache.Cache()

  def rom_for_path(self, console, path):
    return model.ROM(
      name    = self.parser.parse(path),
      path    = path,
      console = console
    )

  def _search(self, roms_directory, console):
    cached_result = self.search_cache.get(roms_directory, console.fullname)
    if cached_result is not None:
      logger.debug("[%s] Using cached result for console" % (console.shortname))

    logger.debug("[%s] Actually performing search for ROMs")
    paths = self.filesystem.files_in_directory(roms_directory, include_subdirectories=True)
    logger.debug("[%s] Files in ROMs directory: %s" % (console.shortname, paths))
    valid_rom_paths = filter(partial(consoles.path_is_rom, console), paths)
    logger.debug("[%s] Filtered list of paths to ROMs: %s" % (console.shortname, valid_rom_paths))

    result = map(partial(self.rom_for_path, console), valid_rom_paths)
    self.search_cache.set(roms_directory, console.fullname, result)
    return result

  def roms_for_console(self, config, console):
    """
    @param console - A console object
    @returns A list of ROM objects representing all of the valid ROMs for a
             given console.

    Valid ROMs are defined as ROMs for which the function `path_is_rom` returns
    True when given the console.

    Returns an empty list if `console` is not enabled
    """
    roms_directory = consoles.console_roms_directory(config, console)
    logger.debug("[%s] Using `%s` as ROMs directory" % (console.shortname, roms_directory))
    return self._search(roms_directory, console)

  def roms_for_consoles(self, config, consoles):
    """
    @param consoles - An iterable list of consoles
    @returns A list of all of the ROMs for all of the consoles in `consoles`

    Equivalent to calling `roms_for_console` on every element of `consoles`
    and combining the results
    """
    # Abuses the fact that the `+` operator is overloaded with lists to turn
    # our list of lists into a single giant list. Yay for duck typing?
    return sum(map(partial(self.roms_for_console, config), consoles), [])
