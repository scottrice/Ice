
import mock
import unittest

from ice import steam_shortcut_synchronizer
from ice.rom import ICE_FLAG_TAG
from pysteam.shortcut import Shortcut


class SteamShortcutSynchronizerTests(unittest.TestCase):

  def setUp(self):
    self.mock_user = mock.MagicMock()
    self.mock_logger = mock.MagicMock()
    self.synchronizer = steam_shortcut_synchronizer.SteamShortcutSynchronizer(self.mock_logger)

  def test_unmanaged_shortcuts_returns_shortcut_not_affiliated_with_ice(self):
    random_shortcut = Shortcut("Plex", "/Some/Random/Path/plex", "/Some/Random/Path")
    self.assertEquals(self.synchronizer.unmanaged_shortcuts([random_shortcut]), [random_shortcut])

  def test_unmanaged_shortcuts_doesnt_return_shortcut_with_flag_tag(self):
    tagged_shortcut = Shortcut("Game", "/Path/to/game", "/Path/to", "", ICE_FLAG_TAG)
    self.assertEquals(self.synchronizer.unmanaged_shortcuts([tagged_shortcut]), [])

  def test_added_shortcuts_doesnt_return_shortcuts_that_still_exist(self):
    shortcut1 = Shortcut("Game1", "/Path/to/game1", "/Path/to", "", ICE_FLAG_TAG)
    shortcut2 = Shortcut("Game2", "/Path/to/game2", "/Path/to", "", ICE_FLAG_TAG)
    old = [shortcut1, shortcut2]
    new = [shortcut1, shortcut2]
    self.assertEquals(self.synchronizer.added_shortcuts(old, new), [])

  def test_added_shortcuts_returns_shortcuts_that_didnt_exist_previously(self):
    shortcut1 = Shortcut("Game1", "/Path/to/game1", "/Path/to", "", ICE_FLAG_TAG)
    shortcut2 = Shortcut("Game2", "/Path/to/game2", "/Path/to", "", ICE_FLAG_TAG)
    new = [shortcut1, shortcut2]
    self.assertEquals(self.synchronizer.added_shortcuts([], new), [shortcut1, shortcut2])

  def test_added_shortcuts_only_returns_shortcuts_that_exist_now_but_not_before(self):
    shortcut1 = Shortcut("Game1", "/Path/to/game1", "/Path/to", "", ICE_FLAG_TAG)
    shortcut2 = Shortcut("Game2", "/Path/to/game2", "/Path/to", "", ICE_FLAG_TAG)
    shortcut3 = Shortcut("Game3", "/Path/to/game3", "/Path/to", "", ICE_FLAG_TAG)
    shortcut4 = Shortcut("Game4", "/Path/to/game4", "/Path/to", "", ICE_FLAG_TAG)
    old = [shortcut1, shortcut2]
    new = [shortcut1, shortcut2, shortcut3, shortcut4]
    self.assertEquals(self.synchronizer.added_shortcuts(old, new), [shortcut3, shortcut4])

  def test_removed_shortcuts_doesnt_return_shortcuts_that_still_exist(self):
    shortcut1 = Shortcut("Game1", "/Path/to/game1", "/Path/to", "", ICE_FLAG_TAG)
    shortcut2 = Shortcut("Game2", "/Path/to/game2", "/Path/to", "", ICE_FLAG_TAG)
    old = [shortcut1, shortcut2]
    new = [shortcut1, shortcut2]
    self.assertEquals(self.synchronizer.removed_shortcuts(old, new), [])

  def test_removed_shortcuts_returns_shortcuts_that_dont_exist_anymore(self):
    shortcut1 = Shortcut("Game1", "/Path/to/game1", "/Path/to", "", ICE_FLAG_TAG)
    shortcut2 = Shortcut("Game2", "/Path/to/game2", "/Path/to", "", ICE_FLAG_TAG)
    old = [shortcut1, shortcut2]
    new = []
    self.assertEquals(self.synchronizer.removed_shortcuts(old, new), [shortcut1, shortcut2])

  def test_removed_shortcuts_only_returns_shortcuts_that_dont_exist_now_but_did_before(self):
    shortcut1 = Shortcut("Game1", "/Path/to/game1", "/Path/to", "", ICE_FLAG_TAG)
    shortcut2 = Shortcut("Game2", "/Path/to/game2", "/Path/to", "", ICE_FLAG_TAG)
    shortcut3 = Shortcut("Game3", "/Path/to/game3", "/Path/to", "", ICE_FLAG_TAG)
    shortcut4 = Shortcut("Game4", "/Path/to/game4", "/Path/to", "", ICE_FLAG_TAG)
    old = [shortcut1, shortcut2, shortcut3, shortcut4]
    new = [shortcut1, shortcut2]
    self.assertEquals(self.synchronizer.removed_shortcuts(old, new), [shortcut3, shortcut4])

  def test_sync_roms_for_user_keeps_unmanaged_shortcuts(self):
    random_shortcut = Shortcut("Plex", "/Some/Random/Path/plex", "/Some/Random/Path")
    self.mock_user.shortcuts = [random_shortcut]

    shortcut1 = Shortcut("Game1", "/Path/to/game1", "/Path/to", "", ICE_FLAG_TAG)
    shortcut2 = Shortcut("Game2", "/Path/to/game2", "/Path/to", "", ICE_FLAG_TAG)
    shortcut3 = Shortcut("Game3", "/Path/to/game3", "/Path/to", "", ICE_FLAG_TAG)
    shortcut4 = Shortcut("Game4", "/Path/to/game4", "/Path/to", "", ICE_FLAG_TAG)

    rom1 = mock.MagicMock()
    rom1.to_shortcut.return_value = shortcut1
    rom2 = mock.MagicMock()
    rom2.to_shortcut.return_value = shortcut2
    rom3 = mock.MagicMock()
    rom3.to_shortcut.return_value = shortcut3
    rom4 = mock.MagicMock()
    rom4.to_shortcut.return_value = shortcut4

    self.synchronizer.sync_roms_for_user(self.mock_user, [rom1, rom2, rom3, rom4])
    new_shortcuts = self.mock_user.shortcuts

    self.assertEquals(len(new_shortcuts), 5)
    self.assertIn(random_shortcut, new_shortcuts)
    self.assertIn(shortcut1, new_shortcuts)
    self.assertIn(shortcut2, new_shortcuts)
    self.assertIn(shortcut3, new_shortcuts)
    self.assertIn(shortcut4, new_shortcuts)
