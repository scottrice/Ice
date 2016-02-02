
import os
import shutil
import tempfile
import unittest

from mockito import *

from nose_parameterized import parameterized

from pysteam import model as steam_model

from ice import model
from ice import paths
from ice import roms

from testinfra import fixtures

class ROMsTests(unittest.TestCase):

  def setUp(self):
    pass

  @parameterized.expand([
    (None, paths.default_roms_directory()),
    ("", paths.default_roms_directory()),
    ('/roms/', '/roms/'),
  ])
  def test_roms_directory(self, config_directory, expected):
    config = mock()
    config.roms_directory = config_directory
    self.assertEqual(roms.roms_directory(config), expected)

  @parameterized.expand([
    ('Banjo Kazoomie', None, 'Banjo Kazoomie'),
    ('Banjo Kazoomie', '[Vapor]', '[Vapor] Banjo Kazoomie'),
    ('Game Name', '!Something!', '!Something! Game Name'),
  ])
  def test_rom_shortcut_name(self, name, console_prefix, expected):
    console = model.Console(
      fullname = 'Nintendo Entertainment System',
      shortname = 'NES',
      extensions = '',
      custom_roms_directory = '',
      prefix = console_prefix,
      icon = '',
      images_directory = '',
      emulator = None,
    )
    rom = model.ROM(
      name = name,
      path = '/Path/to/ROM',
      console = console
    )
    self.assertEqual(roms.rom_shortcut_name(rom), expected)

  @parameterized.expand([
    (fixtures.roms.banjo_kazooie, steam_model.Shortcut(
      name = '[NES] Banjo Kazooie',
      exe = '\"/emulators/Mednafen/mednafen\" \"/roms/nes/Banjo Kazooie.nes\"',
      startdir = '/emulators/Mednafen',
      icon = '/consoles/icons/nes.png',
      tags = ['Nintendo Entertainment System']
    ))
  ])
  def test_rom_to_shortcut(self, rom, expected):
    self.assertEqual(roms.rom_to_shortcut(rom), expected)
