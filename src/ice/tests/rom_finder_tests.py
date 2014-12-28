
import mock
import os
import shutil
import tempfile
import unittest

from ice import rom_finder


class ROMFinderTests(unittest.TestCase):

  def setUp(self):
    self.mock_console = mock.MagicMock()
    self.mock_filesystem = mock.MagicMock()
    self.rom_finder = rom_finder.ROMFinder(self.mock_filesystem)

  def tearDown(self):
    pass

  def test_roms_for_console_returns_a_rom_for_every_file_in_roms_directory(
          self):
    dirname = "RandomDir"
    rom1 = os.path.join(dirname, "rom1")
    rom2 = os.path.join(dirname, "rom2")
    rom3 = os.path.join(dirname, "rom3")
    rom_paths = [rom1, rom2, rom3]
    self.mock_console.is_valid_rom.return_value = True
    self.mock_console.roms_directory.return_value = dirname
    self.mock_filesystem.files_in_directory.return_value = rom_paths

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
    self.mock_console.is_valid_rom.return_value = False
    self.mock_console.roms_directory.return_value = dirname
    self.mock_filesystem.files_in_directory.return_value = rom_paths

    self.assertEquals([], self.rom_finder.roms_for_console(self.mock_console))

  def test_roms_for_console_returns_nothing_for_disabled_consoles(self):
    dirname = "RandomDir"
    rom1 = os.path.join(dirname, "rom1")
    rom2 = os.path.join(dirname, "rom2")
    rom3 = os.path.join(dirname, "rom3")
    rom_paths = [rom1, rom2, rom3]
    self.mock_filesystem.files_in_directory.return_value = rom_paths

    console = mock.MagicMock()
    console.is_enabled.return_value = False
    self.assertEquals(self.rom_finder.roms_for_console(console), [])

  def test_roms_for_consoles_returns_collection_of_all_roms(self):
    firstdir = "RandomDir"
    rom1 = os.path.join(firstdir, "rom1")
    rom2 = os.path.join(firstdir, "rom2")
    seconddir = "RandomDir2"
    rom3 = os.path.join(seconddir, "rom3")
    rom_paths = [rom1, rom2, rom3]

    def fake_files_in_directory(dirname):
      return [rom1, rom2] if dirname == firstdir else [rom3]
    self.mock_filesystem.files_in_directory.side_effect = fake_files_in_directory

    console1 = mock.MagicMock()
    console1.roms_directory.return_value = firstdir
    console2 = mock.MagicMock()
    console2.roms_directory.return_value = seconddir
    both_consoles = [console1, console2]

    roms = self.rom_finder.roms_for_consoles([console1])
    self.assertEquals(len(roms), 2)
    for rom in roms:
      self.assertIn(rom.path, rom_paths)
      self.assertEquals(rom.console, console1)

    roms = self.rom_finder.roms_for_consoles(both_consoles)
    self.assertEquals(len(roms), 3)
    for rom in roms:
      self.assertIn(rom.path, rom_paths)
      self.assertIn(rom.console, both_consoles)
