# encoding: utf-8
"""
local_provider_tests.py

Created by Scott on 2014-08-18.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from mockito import *
import os
import shutil
import tempfile
import unittest

from ice.gridproviders.local_provider import LocalProvider


class LocalProviderTests(unittest.TestCase):

  def setUp(self):
    self.provider = LocalProvider()
    self.temp_directory = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.temp_directory)

  def create_mock_rom(self, rom_name="Test ROM", console_shortname="Test"):
    mock_console = mock()
    mock_console.shortname = console_shortname
    mock_console.images_directory = self.temp_directory
    mock_rom = mock()
    mock_rom.name = rom_name
    mock_rom.console = mock_console
    return mock_rom

  def make_temp_image(self, filename):
    path = os.path.join(self.temp_directory, filename)
    f = open(path, "w")
    f.write("Data")
    f.close()

  def test_is_enabled_returns_true(self):
    self.assertTrue(self.provider.is_enabled())

  def test_returns_none_when_no_images(self):
    rom = self.create_mock_rom("Megaman")
    self.assertIsNone(self.provider.image_for_rom(rom))

  def test_returns_image_with_png_extension(self):
    rom = self.create_mock_rom("Megaman")
    self.make_temp_image("Megaman.png")
    self.assertIsNotNone(self.provider.image_for_rom(rom))

  def test_returns_image_with_jpg_extension(self):
    rom = self.create_mock_rom("Megaman")
    self.make_temp_image("Megaman.jpg")
    self.assertIsNotNone(self.provider.image_for_rom(rom))

  def test_returns_image_with_jpeg_extension(self):
    rom = self.create_mock_rom("Megaman")
    self.make_temp_image("Megaman.jpeg")
    self.assertIsNotNone(self.provider.image_for_rom(rom))

  def test_returns_image_with_tiff_extension(self):
    rom = self.create_mock_rom("Megaman")
    self.make_temp_image("Megaman.tiff")
    self.assertIsNotNone(self.provider.image_for_rom(rom))

  def test_ignores_image_with_invalid_extension(self):
    rom = self.create_mock_rom("Megaman")
    self.make_temp_image("Megaman.gif")
    self.assertIsNone(self.provider.image_for_rom(rom))

  def test_ignores_directories_with_names_like_files(self):
    rom = self.create_mock_rom("Megaman")
    os.mkdir(os.path.join(self.temp_directory, "Megaman.png"))
    self.assertIsNone(self.provider.image_for_rom(rom))

  def test_returns_none_when_no_image_directory(self):
    rom = self.create_mock_rom("Megaman")
    rom.console.images_directory = ""
    self.assertIsNone(self.provider.image_for_rom(rom))
