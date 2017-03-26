
import os
import tempfile
import unittest

from mockito import *
from nose_parameterized import parameterized

from ice import emulators
from ice import model

class EmulatorsTests(unittest.TestCase):

  @parameterized.expand([
    ("C:/emu.exe", "C:/"),
    ("C:/Path/to/emulator.exe", "C:/Path/to"),
    ("/emu", "/"),
    ("/path/to/emulator", "/path/to"),
  ])
  def test_emulator_startdir(self, location, expected):
    emu = model.Emulator("Mednafen", location, "%l %r")
    self.assertEqual(emulators.emulator_startdir(emu), expected)

  @parameterized.expand([
    ("%r", "/emu", "/ROMs/rom", "\"/ROMs/rom\""),
    # Locations that contain quotes
    ("%r", "\"/emu\"", "/ROMs/rom", "\"/ROMs/rom\""),
  ])
  def test_emulator_rom_launch_options(self, fmt, location, rompath, expected):
    emu = model.Emulator("Mednafen", location, fmt)
    r = model.ROM(
      name = "ROM",
      path = rompath,
      console = mock(),
    )
    self.assertEqual(emulators.emulator_rom_launch_options(emu, r), expected)
