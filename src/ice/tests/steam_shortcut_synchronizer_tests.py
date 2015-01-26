
import mock
import unittest

from ice import steam_shortcut_synchronizer
from ice.rom import ICE_FLAG_TAG
from pysteam.shortcut import Shortcut


class SteamShortcutSynchronizerTests(unittest.TestCase):

  def setUp(self):
    self.mock_user = mock.MagicMock()
    self.mock_archive = mock.MagicMock()
    self.mock_logger = mock.MagicMock()
    self.synchronizer = steam_shortcut_synchronizer.SteamShortcutSynchronizer(self.mock_archive, self.mock_logger)

  def test_unmanaged_shortcuts_returns_shortcut_not_affiliated_with_ice(self):
    random_shortcut = Shortcut("Plex", "/Some/Random/Path/plex", "/Some/Random/Path")
    unmanaged = self.synchronizer.unmanaged_shortcuts([],[random_shortcut])
    self.assertEquals(unmanaged, [random_shortcut])

  def test_unmanaged_shortcuts_doesnt_return_shortcut_with_flag_tag(self):
    tagged_shortcut = Shortcut("Game", "/Path/to/game", "/Path/to", "", ICE_FLAG_TAG)
    unmanaged = self.synchronizer.unmanaged_shortcuts([],[tagged_shortcut])
    self.assertEquals(unmanaged, [])

  def test_unmanaged_shortcuts_doesnt_return_shortcut_with_appid_in_managed_ids(self):
    managed_shortcut = Shortcut("Game", "/Path/to/game", "/Path/to", "")
    random_shortcut = Shortcut("Plex", "/Some/Random/Path/plex", "/Some/Random/Path")
    managed_ids = [managed_shortcut.appid()]
    shortcuts = [managed_shortcut, random_shortcut]
    unmanaged = self.synchronizer.unmanaged_shortcuts(managed_ids,shortcuts)
    self.assertEquals(unmanaged, [random_shortcut])

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

  def test_sync_roms_for_user_logs_when_a_rom_is_added(self):
    shortcut = Shortcut("Game", "/Path/to/game", "/Path/to", "", ICE_FLAG_TAG)
    rom = mock.MagicMock()
    rom.to_shortcut.return_value = shortcut

    self.synchronizer.sync_roms_for_user(self.mock_user, [rom])
    self.assertTrue(self.mock_logger.info.called)

  def test_sync_roms_for_user_logs_once_for_each_added_rom(self):
    shortcut1 = Shortcut("Game1", "/Path/to/game1", "/Path/to", "", ICE_FLAG_TAG)
    rom1 = mock.MagicMock()
    rom1.to_shortcut.return_value = shortcut1
    shortcut2 = Shortcut("Game2", "/Path/to/game2", "/Path/to", "", ICE_FLAG_TAG)
    rom2 = mock.MagicMock()
    rom2.to_shortcut.return_value = shortcut2
    shortcut3 = Shortcut("Game3", "/Path/to/game3", "/Path/to", "", ICE_FLAG_TAG)
    rom3 = mock.MagicMock()
    rom3.to_shortcut.return_value = shortcut3

    self.synchronizer.sync_roms_for_user(self.mock_user, [rom1, rom2, rom3])
    self.assertEquals(self.mock_logger.info.call_count, 3)

  def test_sync_roms_for_user_logs_when_a_rom_is_removed(self):
    shortcut = Shortcut("Game", "/Path/to/game", "/Path/to", "", ICE_FLAG_TAG)
    self.mock_user.shortcuts = [shortcut]

    self.synchronizer.sync_roms_for_user(self.mock_user, [])
    self.assertTrue(self.mock_logger.info.called)

  def test_sync_roms_for_user_logs_once_for_each_removed_rom(self):
    shortcut1 = Shortcut("Game1", "/Path/to/game1", "/Path/to", "", ICE_FLAG_TAG)
    shortcut2 = Shortcut("Game2", "/Path/to/game2", "/Path/to", "", ICE_FLAG_TAG)
    shortcut3 = Shortcut("Game3", "/Path/to/game3", "/Path/to", "", ICE_FLAG_TAG)
    self.mock_user.shortcuts = [shortcut1, shortcut2, shortcut3]

    self.synchronizer.sync_roms_for_user(self.mock_user, [])
    self.assertEquals(self.mock_logger.info.call_count, 3)

  def test_sync_roms_for_user_both_adds_and_removes_roms(self):
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

    old_shortcuts = [shortcut1, shortcut2, shortcut4]
    self.mock_user.shortcuts = old_shortcuts
    self.synchronizer.sync_roms_for_user(self.mock_user, [rom1, rom2, rom3])
    new_shortcuts = self.mock_user.shortcuts

    self.assertEquals(self.mock_logger.info.call_count, 2)
    self.assertEquals(len(new_shortcuts), 3)
    self.assertIn(shortcut1, new_shortcuts)
    self.assertIn(shortcut2, new_shortcuts)
    self.assertIn(shortcut3, new_shortcuts)

  def test_sync_roms_for_user_saves_shortcuts_after_running(self):
    shortcut1 = Shortcut("Game1", "/Path/to/game1", "/Path/to", "", ICE_FLAG_TAG)
    rom1 = mock.MagicMock()
    rom1.to_shortcut.return_value = shortcut1

    self.mock_user.shortcuts = []
    self.synchronizer.sync_roms_for_user(self.mock_user, [rom1])

    self.assertEquals(self.mock_user.shortcuts, [shortcut1])
    self.assertTrue(self.mock_user.save_shortcuts.called)
