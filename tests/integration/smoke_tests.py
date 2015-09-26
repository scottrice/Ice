
import os
import unittest

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
