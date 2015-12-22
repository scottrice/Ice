
import os
import tempfile
import unittest

from mockito import *

from pysteam import grid
from pysteam import model
from pysteam import shortcuts

from ice import steam_grid_updater

from testinfra import fixtures

class SteamGridUpdaterTests(unittest.TestCase):

  def setUp(self):
    self.steam_fixture = fixtures.SteamFixture()
    self.user_fixture = fixtures.UserFixture(self.steam_fixture)

    self.mock_logger = mock()
    self.mock_provider = mock()
    self.updater = steam_grid_updater.SteamGridUpdater(
        self.mock_provider,
        self.mock_logger,
    )

  def tearDown(self):
    self.user_fixture.tearDown()
    self.steam_fixture.tearDown()

  def test_updater_sets_image_if_provider_has_one(self):
    shortcut = model.Shortcut("Plex", "Plex.exe", "/Path/to/", "", [])

    rom = mock()
    when(rom).to_shortcut().thenReturn(shortcut)

    (handle, path) = tempfile.mkstemp('.png')
    when(self.mock_provider).image_for_rom(rom).thenReturn(path)

    self.assertFalse(grid.has_custom_image(self.user_fixture.get_context(), shortcuts.shortcut_app_id(shortcut)))
    self.updater.update_rom_artwork(self.user_fixture.get_context(), rom)
    self.assertTrue(grid.has_custom_image(self.user_fixture.get_context(), shortcuts.shortcut_app_id(shortcut)))

  def test_updater_does_nothing_if_provider_has_no_image(self):
    shortcut = model.Shortcut("Plex", "Plex.exe", "/Path/to/", "", [])

    rom = mock()
    when(rom).to_shortcut().thenReturn(shortcut)

    when(self.mock_provider).image_for_rom(rom).thenReturn(None)

    self.assertFalse(grid.has_custom_image(self.user_fixture.get_context(), shortcuts.shortcut_app_id(shortcut)))
    self.updater.update_rom_artwork(self.user_fixture.get_context(), rom)

    self.assertFalse(grid.has_custom_image(self.user_fixture.get_context(), shortcuts.shortcut_app_id(shortcut)))
