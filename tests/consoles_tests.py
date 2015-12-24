
import unittest

from mockito import *
from nose_parameterized import parameterized

from ice import consoles
from ice import model
from ice import rom

class ConsolesTests(unittest.TestCase):

  def test_console_is_enabled(self):
    emu = mock()
    valid = model.Console("Nintendo", "NES", "", "", "", "", "", emu)
    self.assertTrue(consoles.console_is_enabled(valid))

    invalid = model.Console("Nintendo", "NES", "", "", "", "", "", None)
    self.assertFalse(consoles.console_is_enabled(invalid))

  @parameterized.expand([
    # No extensions passes everything
    ("", "/Games/rom.txt", True),
    # Extensions that dont exist in the list dont pass
    ("nes", "/Games/rom.txt", False),
    ("nes, snes, n64", "/Games/rom.exe", False),
    # Extensions that exist in the list are fine
    ("nes", "/Games/rom.nes", True),
    ("nes, snes, n64", "/Games/rom.snes", True),
    # Even if they have a leading .
    (".nes, .snes, n64", "/Games/rom.n64", True),
    (".nes, .snes, n64", "/Games/rom.snes", True),
    # And even if the capitalization is screwy
    ("NES, .snes", "/Games/ROM.SNES", True),
    ("NES, .snes", "/Games/ROM.nEs", True),
    # Also with stupid whitespace
    ("NES,       .snes", "/Games/ROM.SNES", True),
  ])
  def test_path_is_rom(self, extensions, path, expected):
    console = model.Console("Nintendo", "NES", extensions, "", "", "", "", None)
    self.assertEqual(consoles.path_is_rom(console, path), expected)
