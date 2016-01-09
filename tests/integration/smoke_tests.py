
import os
import unittest

from pysteam import model

from ..testinfra.fake_environment import FakeEnvironment

class SmokeTests(unittest.TestCase):

  def setUp(self):
    self.env = FakeEnvironment(__file__)

  def tearDown(self):
    self.env.clean()

  def test_add_single_rom(self):
    self.env.load_test_data(os.path.join("smoke", "adding_single_rom"))
    u1 = self.env.create_fake_user()
    self.env.run_command()
    self.assertEqual(self.env.user_shortcuts(u1), self.env.expected_shortcuts())

  def test_add_rom_for_two_users_with_different_preexisting_shortcuts(self):
    self.env.load_test_data(os.path.join("smoke", "adding_single_rom"))
    u1 = self.env.create_fake_user()
    u2 = self.env.create_fake_user()
    u2_shortcut = model.Shortcut('Plex', '/Path/to/Plex', '/Path/to', '', [])
    preexisting_shortcuts = [u2_shortcut]
    self.env.set_user_shortcuts(u2, preexisting_shortcuts)
    self.env.run_command()
    expected = self.env.expected_shortcuts()

    u1_synced_shortcuts = self.env.user_shortcuts(u1)
    self.assertNotIn(u2_shortcut, u1_synced_shortcuts)
    for shortcut in expected:
      self.assertIn(shortcut, u1_synced_shortcuts)

    u2_synced_shortcuts = self.env.user_shortcuts(u2)
    self.assertIn(u2_shortcut, u2_synced_shortcuts)
    for shortcut in expected:
      self.assertIn(shortcut, u2_synced_shortcuts)
