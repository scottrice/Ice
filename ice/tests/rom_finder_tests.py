
from mockito import *
import os
import shutil
import tempfile
import unittest

from ice import rom_finder


class ROMFinderTests(unittest.TestCase):

  def setUp(self):
    self.mock_console = mock()
    self.mock_config = mock()
    self.mock_filesystem = mock()
    self.mock_parser = mock()
    self.rom_finder = rom_finder.ROMFinder(
      self.mock_config,
      self.mock_filesystem,
      self.mock_parser,
    )

  def test_roms_for_console_returns_a_rom_for_every_file_in_roms_directory(self):
    dirname = "RandomDir"
    rom1 = os.path.join(dirname, "rom1")
    rom2 = os.path.join(dirname, "rom2")
    rom3 = os.path.join(dirname, "rom3")
    rom_paths = [rom1, rom2, rom3]

    when(self.mock_console).is_enabled().thenReturn(True)
    when(self.mock_console).is_valid_rom(any()).thenReturn(True)
    when(self.mock_config).roms_directory_for_console(self.mock_console).thenReturn(dirname)
    when(self.mock_filesystem).files_in_directory(dirname, include_subdirectories=True).thenReturn(rom_paths)

    roms = self.rom_finder.roms_for_console(self.mock_console)
    self.assertEquals(len(roms), 3)
    for rom in roms:
      self.assertIn(rom.path, rom_paths)
      self.assertEquals(rom.console, self.mock_console)

  def test_roms_for_console_ignores_invalid_roms(self):
    dirname = "RandomDir"
    rom1 = os.path.join(dirname, "rom1")
    rom2 = os.path.join(dirname, "rom2")
    rom3 = os.path.join(dirname, "rom3")
    rom_paths = [rom1, rom2, rom3]

    when(self.mock_console).is_enabled().thenReturn(True)
    when(self.mock_console).is_valid_rom(any()).thenReturn(False)
    when(self.mock_config).roms_directory_for_console(self.mock_console).thenReturn(dirname)
    when(self.mock_filesystem).files_in_directory(dirname, include_subdirectories=True).thenReturn(rom_paths)

    self.assertEquals([], self.rom_finder.roms_for_console(self.mock_console))

  def test_roms_for_console_returns_nothing_for_disabled_consoles(self):
    dirname = "RandomDir"
    rom1 = os.path.join(dirname, "rom1")
    rom2 = os.path.join(dirname, "rom2")
    rom3 = os.path.join(dirname, "rom3")
    rom_paths = [rom1, rom2, rom3]
    self.mock_filesystem.files_in_directory.return_value = rom_paths

    when(self.mock_console).is_enabled().thenReturn(False)
    self.assertEquals(self.rom_finder.roms_for_console(self.mock_console), [])

  def test_roms_for_consoles_returns_roms_in_subdirs(self):
    firstdir = "RandomDir"
    rom1 = os.path.join(firstdir, "rom1")
    subdir = "RandomSubdir"
    rom2 = os.path.join(firstdir, subdir, "rom2")
    rom_paths = [rom1, rom2]

    when(self.mock_console).is_enabled().thenReturn(True)
    when(self.mock_console).is_valid_rom(any()).thenReturn(True)
    when(self.mock_config).roms_directory_for_console(self.mock_console).thenReturn(firstdir)
    when(self.mock_filesystem).files_in_directory(firstdir, include_subdirectories=True).thenReturn(rom_paths)

    roms = self.rom_finder.roms_for_console(self.mock_console)
    self.assertEquals(len(roms), 2)
    [self.assertIn(rom.path, rom_paths) for rom in roms]

  def test_roms_for_consoles_returns_collection_of_all_roms(self):
    firstdir = "RandomDir"
    rom1 = os.path.join(firstdir, "rom1")
    rom2 = os.path.join(firstdir, "rom2")

    seconddir = "RandomDir2"
    rom3 = os.path.join(seconddir, "rom3")

    rom_paths = [rom1, rom2, rom3]

    when(self.mock_filesystem).files_in_directory(firstdir, include_subdirectories=True).thenReturn([rom1, rom2])
    when(self.mock_filesystem).files_in_directory(seconddir, include_subdirectories=True).thenReturn([rom3])

    console1 = mock()
    when(console1).is_enabled().thenReturn(True)
    when(console1).is_valid_rom(any()).thenReturn(True)

    console2 = mock()
    when(console2).is_enabled().thenReturn(True)
    when(console2).is_valid_rom(any()).thenReturn(True)

    when(self.mock_config).roms_directory_for_console(console1).thenReturn(firstdir)
    when(self.mock_config).roms_directory_for_console(console2).thenReturn(seconddir)

    roms = self.rom_finder.roms_for_consoles([console1])
    self.assertEquals(len(roms), 2)
    for rom in roms:
      self.assertIn(rom.path, rom_paths)
      self.assertEquals(rom.console, console1)

    both_consoles = [console1, console2]
    roms = self.rom_finder.roms_for_consoles(both_consoles)
    self.assertEquals(len(roms), 3)
    for rom in roms:
      self.assertIn(rom.path, rom_paths)
      self.assertIn(rom.console, both_consoles)

  def test_uses_parser_to_determine_rom_name(self):
    dirname = "RandomDir"
    rom1 = os.path.join(dirname, "rom1")
    rom_paths = [rom1]

    when(self.mock_console).is_enabled().thenReturn(True)
    when(self.mock_console).is_valid_rom(rom1).thenReturn(True)
    when(self.mock_config).roms_directory_for_console(self.mock_console).thenReturn(dirname)
    when(self.mock_filesystem).files_in_directory(dirname, include_subdirectories=True).thenReturn(rom_paths)
    when(self.mock_parser).parse(any(str)).thenReturn("ROM Name")

    roms = self.rom_finder.roms_for_console(self.mock_console)
    self.assertEquals(len(roms), 1)
    returned_rom = roms[0]
    self.assertEquals(returned_rom.name, "ROM Name")
