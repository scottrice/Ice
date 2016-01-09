
import unittest

from mockito import *

from pysteam import model as steam_model
from pysteam import shortcuts

from ice import model
from ice import steam_shortcut_synchronizer
from ice import roms

from testinfra import fixtures

class SteamShortcutSynchronizerTests(unittest.TestCase):

  def setUp(self):
    self.steam_fixture = fixtures.SteamFixture()
    self.user_fixture = fixtures.UserFixture(self.steam_fixture)

    self.mock_archive = mock()
    self.mock_logger = mock()
    self.synchronizer = steam_shortcut_synchronizer.SteamShortcutSynchronizer(self.mock_archive, self.mock_logger)

  def tearDown(self):
    self.user_fixture.tearDown()
    self.steam_fixture.tearDown()

  def _set_users_shortcuts(self, users_shortcuts):
    shortcuts.set_shortcuts(self.user_fixture.get_context(), users_shortcuts)

  def _create_dummy_configuration_with_roms_dir(self, roms_dir):
    config = mock()
    # We check the path of every console (so we need at least 1 to do anything),
    # but since we are stubbing our `roms_directory_for_console` impl we don't
    # actually care what the console is.
    console = mock()
    config.console_manager = [ console ]
    when(config).roms_directory_for_console(console).thenReturn(roms_dir)
    return config

  def test_unmanaged_shortcuts_returns_all_shortcuts_when_given_no_history(self):
    mock_config = self._create_dummy_configuration_with_roms_dir("/Some/Other/Path")
    random_shortcut = steam_model.Shortcut("Plex", "/Some/Random/Path/plex", "/Some/Random/Path", "", [])

    unmanaged = self.synchronizer.unmanaged_shortcuts(None ,[random_shortcut], mock_config)

    self.assertEquals(unmanaged, [random_shortcut])

  def test_unmanaged_shortcuts_filters_suspicious_shortcuts_when_given_no_history(self):
    mock_config = self._create_dummy_configuration_with_roms_dir("/Some/Path")
    random_shortcut = steam_model.Shortcut("Iron Man", "/Some/Emulator/Path/emulator /Some/Path/Iron Man", "/Some/Emulator/Path", "", [])

    unmanaged = self.synchronizer.unmanaged_shortcuts(None ,[random_shortcut], mock_config)

    self.assertEquals(unmanaged, [])

  def test_unmanaged_shortcuts_doesnt_filter_suspicious_shortcuts_when_we_have_history(self):
    mock_config = self._create_dummy_configuration_with_roms_dir("/Some/Path")
    random_shortcut = steam_model.Shortcut("Iron Man", "/Some/Emulator/Path/emulator /Some/Path/Iron Man", "/Some/Emulator/Path", "", [])

    unmanaged = self.synchronizer.unmanaged_shortcuts([] ,[random_shortcut], mock_config)

    self.assertEquals(unmanaged, [random_shortcut])

  def test_unmanaged_shortcuts_returns_shortcut_not_affiliated_with_ice(self):
    random_shortcut = steam_model.Shortcut("Plex", "/Some/Random/Path/plex", "/Some/Random/Path", "", [])
    unmanaged = self.synchronizer.unmanaged_shortcuts([],[random_shortcut], None)
    self.assertEquals(unmanaged, [random_shortcut])

  def test_unmanaged_shortcuts_doesnt_return_shortcut_with_flag_tag(self):
    tagged_shortcut = steam_model.Shortcut("Game", "/Path/to/game", "/Path/to", "", [roms.ICE_FLAG_TAG])
    unmanaged = self.synchronizer.unmanaged_shortcuts([],[tagged_shortcut], None)
    self.assertEquals(unmanaged, [])

  def test_unmanaged_shortcuts_doesnt_return_shortcut_with_appid_in_managed_ids(self):
    managed_shortcut = steam_model.Shortcut("Game", "/Path/to/game", "/Path/to", "", [])
    random_shortcut = steam_model.Shortcut("Plex", "/Some/Random/Path/plex", "/Some/Random/Path", "", [])
    managed_ids = [shortcuts.shortcut_app_id(managed_shortcut)]
    all_shortcuts = [managed_shortcut, random_shortcut]
    unmanaged = self.synchronizer.unmanaged_shortcuts(managed_ids, all_shortcuts, None)
    self.assertEquals(unmanaged, [random_shortcut])

  def test_added_shortcuts_doesnt_return_shortcuts_that_still_exist(self):
    shortcut1 = steam_model.Shortcut("Game1", "/Path/to/game1", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut2 = steam_model.Shortcut("Game2", "/Path/to/game2", "/Path/to", "", [roms.ICE_FLAG_TAG])
    old = [shortcut1, shortcut2]
    new = [shortcut1, shortcut2]
    self.assertEquals(self.synchronizer.added_shortcuts(old, new), [])

  def test_added_shortcuts_returns_shortcuts_that_didnt_exist_previously(self):
    shortcut1 = steam_model.Shortcut("Game1", "/Path/to/game1", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut2 = steam_model.Shortcut("Game2", "/Path/to/game2", "/Path/to", "", [roms.ICE_FLAG_TAG])
    new = [shortcut1, shortcut2]
    self.assertEquals(self.synchronizer.added_shortcuts([], new), [shortcut1, shortcut2])

  def test_added_shortcuts_only_returns_shortcuts_that_exist_now_but_not_before(self):
    shortcut1 = steam_model.Shortcut("Game1", "/Path/to/game1", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut2 = steam_model.Shortcut("Game2", "/Path/to/game2", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut3 = steam_model.Shortcut("Game3", "/Path/to/game3", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut4 = steam_model.Shortcut("Game4", "/Path/to/game4", "/Path/to", "", [roms.ICE_FLAG_TAG])
    old = [shortcut1, shortcut2]
    new = [shortcut1, shortcut2, shortcut3, shortcut4]
    self.assertEquals(self.synchronizer.added_shortcuts(old, new), [shortcut3, shortcut4])

  def test_removed_shortcuts_doesnt_return_shortcuts_that_still_exist(self):
    shortcut1 = steam_model.Shortcut("Game1", "/Path/to/game1", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut2 = steam_model.Shortcut("Game2", "/Path/to/game2", "/Path/to", "", [roms.ICE_FLAG_TAG])
    old = [shortcut1, shortcut2]
    new = [shortcut1, shortcut2]
    self.assertEquals(self.synchronizer.removed_shortcuts(old, new), [])

  def test_removed_shortcuts_returns_shortcuts_that_dont_exist_anymore(self):
    shortcut1 = steam_model.Shortcut("Game1", "/Path/to/game1", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut2 = steam_model.Shortcut("Game2", "/Path/to/game2", "/Path/to", "", [roms.ICE_FLAG_TAG])
    old = [shortcut1, shortcut2]
    new = []
    self.assertEquals(self.synchronizer.removed_shortcuts(old, new), [shortcut1, shortcut2])

  def test_removed_shortcuts_only_returns_shortcuts_that_dont_exist_now_but_did_before(self):
    shortcut1 = steam_model.Shortcut("Game1", "/Path/to/game1", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut2 = steam_model.Shortcut("Game2", "/Path/to/game2", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut3 = steam_model.Shortcut("Game3", "/Path/to/game3", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut4 = steam_model.Shortcut("Game4", "/Path/to/game4", "/Path/to", "", [roms.ICE_FLAG_TAG])
    old = [shortcut1, shortcut2, shortcut3, shortcut4]
    new = [shortcut1, shortcut2]
    self.assertEquals(self.synchronizer.removed_shortcuts(old, new), [shortcut3, shortcut4])

  def test_sync_roms_for_user_keeps_unmanaged_shortcuts(self):
    random_shortcut = steam_model.Shortcut("Plex", "/Some/Random/Path/plex", "/Some/Random/Path", "", [])
    self._set_users_shortcuts([random_shortcut])
    when(self.mock_archive).previous_managed_ids(self.user_fixture.get_context()).thenReturn([])

    rom1 = model.ROM(name = 'Game1', path = '/Path/to/game1', console = fixtures.consoles.flagged)
    shortcut1 = roms.rom_to_shortcut(rom1)
    rom2 = model.ROM(name = 'Game2', path = '/Path/to/game2', console = fixtures.consoles.flagged)
    shortcut2 = roms.rom_to_shortcut(rom2)
    rom3 = model.ROM(name = 'Game3', path = '/Path/to/game3', console = fixtures.consoles.flagged)
    shortcut3 = roms.rom_to_shortcut(rom3)
    rom4 = model.ROM(name = 'Game4', path = '/Path/to/game4', console = fixtures.consoles.flagged)
    shortcut4 = roms.rom_to_shortcut(rom4)

    self.synchronizer.sync_roms_for_user(self.user_fixture.get_context(), [rom1, rom2, rom3, rom4], None)
    new_shortcuts = shortcuts.get_shortcuts(self.user_fixture.get_context())

    self.assertEquals(len(new_shortcuts), 5)
    self.assertIn(random_shortcut, new_shortcuts)
    self.assertIn(shortcut1, new_shortcuts)
    self.assertIn(shortcut2, new_shortcuts)
    self.assertIn(shortcut3, new_shortcuts)
    self.assertIn(shortcut4, new_shortcuts)

  def test_sync_roms_for_user_logs_when_a_rom_is_added(self):
    self._set_users_shortcuts([])

    rom = model.ROM(name = 'Game1', path = '/Path/to/game1', console = fixtures.consoles.flagged)
    shortcut = roms.rom_to_shortcut(rom)

    self.synchronizer.sync_roms_for_user(self.user_fixture.get_context(), [rom], None)

    verify(self.mock_logger).info(any())

  def test_sync_roms_for_user_logs_once_for_each_added_rom(self):
    self._set_users_shortcuts([])

    rom1 = model.ROM(name = 'Game1', path = '/Path/to/game1', console = fixtures.consoles.flagged)
    shortcut1 = roms.rom_to_shortcut(rom1)
    rom2 = model.ROM(name = 'Game2', path = '/Path/to/game2', console = fixtures.consoles.flagged)
    shortcut2 = roms.rom_to_shortcut(rom2)
    rom3 = model.ROM(name = 'Game3', path = '/Path/to/game3', console = fixtures.consoles.flagged)
    shortcut3 = roms.rom_to_shortcut(rom3)

    self.synchronizer.sync_roms_for_user(self.user_fixture.get_context(), [rom1, rom2, rom3], None)

    verify(self.mock_logger, times=3).info(any())

  def test_sync_roms_for_user_logs_when_a_rom_is_removed(self):
    shortcut = steam_model.Shortcut("Game", "/Path/to/game", "/Path/to", "", [roms.ICE_FLAG_TAG])
    self._set_users_shortcuts([shortcut])

    self.synchronizer.sync_roms_for_user(self.user_fixture.get_context(), [], None)
    verify(self.mock_logger).info(any())

  def test_sync_roms_for_user_logs_once_for_each_removed_rom(self):
    shortcut1 = steam_model.Shortcut("Game1", "/Path/to/game1", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut2 = steam_model.Shortcut("Game2", "/Path/to/game2", "/Path/to", "", [roms.ICE_FLAG_TAG])
    shortcut3 = steam_model.Shortcut("Game3", "/Path/to/game3", "/Path/to", "", [roms.ICE_FLAG_TAG])
    self._set_users_shortcuts([shortcut1, shortcut2, shortcut3])

    self.synchronizer.sync_roms_for_user(self.user_fixture.get_context(), [], None)
    verify(self.mock_logger, times=3).info(any())

  def test_sync_roms_for_user_both_adds_and_removes_roms(self):
    rom1 = model.ROM(name = 'Game1', path = '/Path/to/game1', console = fixtures.consoles.flagged)
    shortcut1 = roms.rom_to_shortcut(rom1)
    rom2 = model.ROM(name = 'Game2', path = '/Path/to/game2', console = fixtures.consoles.flagged)
    shortcut2 = roms.rom_to_shortcut(rom2)
    rom3 = model.ROM(name = 'Game3', path = '/Path/to/game3', console = fixtures.consoles.flagged)
    shortcut3 = roms.rom_to_shortcut(rom3)
    rom4 = model.ROM(name = 'Game4', path = '/Path/to/game4', console = fixtures.consoles.flagged)
    shortcut4 = roms.rom_to_shortcut(rom4)

    old_shortcuts = [shortcut1, shortcut2, shortcut4]
    self._set_users_shortcuts(old_shortcuts)

    self.synchronizer.sync_roms_for_user(self.user_fixture.get_context(), [rom1, rom2, rom3], None)
    new_shortcuts = shortcuts.get_shortcuts(self.user_fixture.get_context())

    verify(self.mock_logger, times=2).info(any())
    self.assertEquals(len(new_shortcuts), 3)
    self.assertIn(shortcut1, new_shortcuts)
    self.assertIn(shortcut2, new_shortcuts)
    self.assertIn(shortcut3, new_shortcuts)

  def test_sync_roms_for_user_saves_shortcuts_after_running(self):
    rom1 = model.ROM(name = 'Game1', path = '/Path/to/game1', console = fixtures.consoles.flagged)
    shortcut1 = roms.rom_to_shortcut(rom1)

    self._set_users_shortcuts([])

    self.synchronizer.sync_roms_for_user(self.user_fixture.get_context(), [rom1], None)

    updated_shortcuts = shortcuts.get_shortcuts(self.user_fixture.get_context())
    self.assertEquals(updated_shortcuts, [shortcut1])

  def test_sync_roms_for_user_sets_managed_ids(self):
    rom1 = model.ROM(name = 'Game1', path = '/Path/to/game1', console = fixtures.consoles.flagged)
    shortcut1 = roms.rom_to_shortcut(rom1)
    rom2 = model.ROM(name = 'Game2', path = '/Path/to/game2', console = fixtures.consoles.flagged)
    shortcut2 = roms.rom_to_shortcut(rom2)

    self._set_users_shortcuts([])

    self.synchronizer.sync_roms_for_user(self.user_fixture.get_context(), [rom1, rom2], None)

    new_managed_ids = map(shortcuts.shortcut_app_id, [shortcut1, shortcut2])
    verify(self.mock_archive).set_managed_ids(self.user_fixture.get_context(), new_managed_ids)
