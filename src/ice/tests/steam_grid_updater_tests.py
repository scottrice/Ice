
import mock
import unittest

from ice import steam_grid_updater
from ice.error import provider_error


class SteamGridUpdaterTests(unittest.TestCase):

  def setUp(self):
    self.mock_logger = mock.MagicMock()
    self.mock_provider = mock.MagicMock()
    self.mock_user = mock.MagicMock()
    self.updater = steam_grid_updater.SteamGridUpdater(
        self.mock_provider,
        self.mock_logger,
    )

  def test_updater_sets_image_if_provider_has_one(self):
    self.mock_provider.image_for_rom.return_value = "Some/Path/String"
    shortcut = mock.MagicMock()
    shortcut.custom_image.return_value = None
    rom = mock.MagicMock()
    rom.to_shortcut.return_value = shortcut

    self.updater.update_rom_artwork(self.mock_user, rom)
    self.assertTrue(shortcut.set_image.called)

  def test_updater_does_nothing_if_provider_has_no_image(self):
    self.mock_provider.image_for_rom.return_value = None
    shortcut = mock.MagicMock()
    shortcut.custom_image.return_value = None
    rom = mock.MagicMock()
    rom.to_shortcut.return_value = shortcut

    self.updater.update_rom_artwork(self.mock_user, rom)
    self.assertFalse(shortcut.set_image.called)
