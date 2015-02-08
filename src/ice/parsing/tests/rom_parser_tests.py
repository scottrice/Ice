
import mock
import unittest

from nose_parameterized import parameterized

from ice.parsing.rom_parser import ROMParser


class ROMFinderTests(unittest.TestCase):
  def setUp(self):
    self.mock_logger = mock.MagicMock()
    self.parser = ROMParser(self.mock_logger)

  @parameterized.expand([
    ("The Legend of Zelda", "The Legend of Zelda"),
    ("/Some/Folder/Structure/The Legend of Zelda", "The Legend of Zelda"),
    ("The Legend of Zelda.nes", "The Legend of Zelda"),
  ])
  def test_parsing(self, input, expected):
    self.assertEquals(expected, self.parser.parse(input))
