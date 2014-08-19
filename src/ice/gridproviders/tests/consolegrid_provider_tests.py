# encoding: utf-8
"""
consolegrid_provider_tests.py

Created by Scott on 2014-08-18.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import mock
import os
import unittest
from urllib2 import URLError

from ice.error.provider_error import ProviderError
from ice.gridproviders import consolegrid_provider

class ConsoleGridProviderTests(unittest.TestCase):
  def setUp(self):
    self.provider = consolegrid_provider.ConsoleGridProvider()

  def tearDown(self):
    pass

  def dummy_urlopen_function(self, code=200, data="Data", err=None):
    def f(url):
      if err:
        raise err
      m = mock.MagicMock()
      m.getcode.return_value = code
      m.read.return_value = data
      return m
    return f

  def create_mock_rom(self, rom_name="Test ROM", console_name="Test"):
    mock_console = mock.MagicMock()
    mock_console.fullname = console_name
    mock_console.shortname = console_name
    mock_rom = mock.MagicMock()
    mock_rom.name.return_value = rom_name
    mock_rom.console = mock_console
    return mock_rom

  def test_is_enabled_returns_true(self):
    self.assertTrue(self.provider.is_enabled())
  
  def test_consolegrid_top_picture_url(self):
    rom = self.create_mock_rom("Megaman")
    url = self.provider.consolegrid_top_picture_url(rom)
    self.assertIn("consolegrid.com", url)
    self.assertIn("game=Megaman", url)
    self.assertIn("console=Test", url)

  def test_consolegrid_top_picture_url_quotes_special_characters(self):
    rom = self.create_mock_rom("Dankey Kang#Country")
    url = self.provider.consolegrid_top_picture_url(rom)
    self.assertNotIn("Dankey Kang#Country", url)
    self.assertIn("Dankey%20Kang%23Country", url)

  def test_find_url_raises_provider_error_on_204(self):
    rom = self.create_mock_rom("Megaman")
    consolegrid_provider.urllib2.urlopen = self.dummy_urlopen_function(204)
    with self.assertRaises(ProviderError):
      self.provider.find_url_for_rom(rom)

  def test_find_url_raises_provider_error_on_urlerror(self):
    rom = self.create_mock_rom("Megaman")
    err = URLError("")
    consolegrid_provider.urllib2.urlopen = self.dummy_urlopen_function(err=err)
    with self.assertRaises(ProviderError):
      self.provider.find_url_for_rom(rom)

  def test_image_for_rom_returns_none_when_empty_image_url(self):
    def dummy_find_url_for_rom(rom):
      return ""
    self.provider.find_url_for_rom = dummy_find_url_for_rom
    self.assertIsNone(self.provider.image_for_rom(None))