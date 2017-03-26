

import os
import shutil
import tempfile
import unittest

from mockito import *

from nose_parameterized import parameterized

from pysteam import model
from pysteam import shortcuts

from ice import backups
from ice import paths

from testinfra import fixtures

class BackupsTests(unittest.TestCase):

  def setUp(self):
    self.steam_fixture = fixtures.SteamFixture()
    self.user_fixture = fixtures.UserFixture(self.steam_fixture)

  @parameterized.expand([
    (None, None),
    ("", backups.default_backups_directory()),
    ("/some/random/dir", "/some/random/dir"),
  ])
  def test_backup_directory(self, config_backups_dir, expected_dir):
    config = mock()
    config.backup_directory = config_backups_dir

    self.assertEqual(backups.backup_directory(config), expected_dir)

  def test_create_backup_of_shortcuts_does_nothing_if_backups_directory_is_none(self):
    config = mock()
    config.backup_directory = None

    user = self.user_fixture.get_context()

    expected_dir = backups.default_backups_directory()
    expected_location = backups.shortcuts_backup_path(expected_dir, user)

    self.assertFalse(os.path.exists(expected_location))
    backups.create_backup_of_shortcuts(config, user)
    self.assertFalse(os.path.exists(expected_location))

  def test_create_backup_of_shortcuts_creates_directory_if_it_doesnt_exist(self):
    tempdir = tempfile.mkdtemp()
    backup_dir = os.path.join(tempdir, "Backups")

    config = mock()
    config.backup_directory = backup_dir

    user = self.user_fixture.get_context()

    self.assertFalse(os.path.exists(backup_dir))
    backups.create_backup_of_shortcuts(config, user)
    self.assertTrue(os.path.exists(backup_dir))

    shutil.rmtree(tempdir)

  def test_create_backup_of_shortcuts_creates_copy_of_shortcuts_at_backup_path(self):
    tempdir = tempfile.mkdtemp()
    backup_dir = os.path.join(tempdir, "Backups")

    config = mock()
    config.backup_directory = backup_dir

    user = self.user_fixture.get_context()

    shortcut = model.Shortcut('Plex', '/Path/to/plex', '/Path/to', '', '', '', False, False, False, 0, [])
    user_shortcuts = [shortcut]

    shortcuts.set_shortcuts(user, user_shortcuts)
    backups.create_backup_of_shortcuts(config, user)

    expected_path = backups.shortcuts_backup_path(backup_dir, user)
    self.assertTrue(os.path.exists(expected_path))
    self.assertEqual(shortcuts.read_shortcuts(expected_path), user_shortcuts)

    shutil.rmtree(tempdir)
