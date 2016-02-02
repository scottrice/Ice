
from mockito import *
import unittest

from nose_parameterized import parameterized

from ice.parsing.rom_parser import ROMParser


class ROMFinderTests(unittest.TestCase):
  def setUp(self):
    self.parser = ROMParser()

  @parameterized.expand([
    ("The Legend of Zelda", "The Legend of Zelda"),
    ("/Some/Folder/Structure/The Legend of Zelda", "The Legend of Zelda"),
    ("The Legend of Zelda.nes", "The Legend of Zelda"),
    ("Super Metroid (JU) [!]" , "Super Metroid"),
    ("Zelda II - The Adventure of Link (USA).nes" , "Zelda II - The Adventure of Link"),
    ("Legend of Zelda, The - Ocarina of Time (Europe) (En,Fr,De).n64" , "Legend of Zelda, The - Ocarina of Time"),
    ("Legend of Zelda, The - Ocarina of Time - Master Quest (USA) (Debug Edition).n64" , "Legend of Zelda, The - Ocarina of Time - Master Quest"),
    ("Shenmue 2 (PAL).iso" , "Shenmue 2"),
    ("Resident Evil Code Veronica (PAL) (UK).iso" , "Resident Evil Code Veronica"),
    ("Chrono Trigger (USA).sfc", "Chrono Trigger"),
    ("Dr. Mario 64.z64", "Dr. Mario 64"),
    # TODO(Wishlist): I'd like to be able to remove the `Rev 1` from the filename, but that is much
    # more complicated than our current strategy of just matching against everything not in parens
    # ("Super Mario World 2 - Yoshi's Island Rev 1 (1995)(Nintendo)(US).sfc", "Super Mario World 2 - Yoshi's Island"),
  ])
  def test_parsing(self, input, expected):
    self.assertEquals(expected, self.parser.parse(input))
