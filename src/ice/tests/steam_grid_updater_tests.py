
from mockito import *
import unittest

from ice import steam_grid_updater


class SteamGridUpdaterTests(unittest.TestCase):

  def setUp(self):
    self.mock_logger = mock()
    self.mock_provider = mock()
    self.mock_user = mock()
    self.updater = steam_grid_updater.SteamGridUpdater(
        self.mock_provider,
        self.mock_logger,
    )

  def test_updater_sets_image_if_provider_has_one(self):
    shortcut = mock()
    when(shortcut).custom_image(self.mock_user).thenReturn(None)

    rom = mock()
    when(rom).to_shortcut().thenReturn(shortcut)

    when(self.mock_provider).image_for_rom(rom).thenReturn("Some/Path/String")

    self.updater.update_rom_artwork(self.mock_user, rom)
    verify(shortcut).set_image(self.mock_user, "Some/Path/String")

  def test_updater_does_nothing_if_provider_has_no_image(self):
    shortcut = mock()
    when(shortcut).custom_image(self.mock_user).thenReturn(None)

    rom = mock()
    when(rom).to_shortcut().thenReturn(shortcut)

    when(self.mock_provider).image_for_rom(rom).thenReturn(None)

    self.updater.update_rom_artwork(self.mock_user, rom)

    verify(shortcut, never).set_image(any(), any())
