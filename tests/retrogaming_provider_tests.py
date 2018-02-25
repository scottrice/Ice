# encoding: utf-8
"""
retrogaming_provider_tests.py

Created by Raphael on 2018-02-24.
"""

import os
import unittest
from mockito import *
from urllib2 import URLError

# I need to do this instead of importing the class explicitly so that I can
# override the urllib2 function.
# TODO: Use dependency injection so I don't need to use that hack.
from ice.gridproviders import retrogaming_provider


class RetroGamingProviderTests(unittest.TestCase):

    def setUp(self):
        self.provider = retrogaming_provider.RetroGamingProvider()

    def tearDown(self):
        pass

    def dummy_urlopen_function(self, code=200, data="Data", err=None):
        def f(url):
          if err:
              raise err
          m = mock()
          when(m).getcode().thenReturn(code)
          when(m).read().thenReturn(data)
          return m
        return f

    def create_mock_rom(self, rom_name="Test ROM", console_name="Test"):
        console = mock()
        console.fullname = console_name
        console.shortname = console_name

        rom = mock()
        rom.name = rom_name
        rom.console = console
        return rom

    def test_is_enabled_returns_true(self):
        self.assertTrue(self.provider.is_enabled())

    def test_retrogaming_top_picture_url(self):
        rom = self.create_mock_rom("Megaman")
        url = self.provider.retrogaming_top_picture_url(rom)
        self.assertIn("retrogaming.cloud", url)
        self.assertIn("game=Megaman", url)
        self.assertIn("console=Test", url)

    def test_retrogaming_top_picture_url_quotes_special_characters(self):
        rom = self.create_mock_rom("Dankey Kang#Country")
        url = self.provider.retrogaming_top_picture_url(rom)
        self.assertNotIn("Dankey Kang#Country", url)
        self.assertIn("Dankey%20Kang%23Country", url)

    def test_find_url_returns_none_on_204(self):
        rom = self.create_mock_rom("Megaman")
        retrogaming_provider.urllib2.urlopen = self.dummy_urlopen_function(204)
        self.assertIsNone(self.provider.find_url_for_rom(rom))

    def test_find_url_returns_none_on_urlerror(self):
        rom = self.create_mock_rom("Megaman")
        err = URLError("")
        retrogaming_provider.urllib2.urlopen = self.dummy_urlopen_function(err=err)
        self.assertIsNone(self.provider.find_url_for_rom(rom))

    def test_image_for_rom_returns_none_when_empty_image_url(self):
        def dummy_find_url_for_rom(rom):
          return ""
        self.provider.find_url_for_rom = dummy_find_url_for_rom
        self.assertIsNone(self.provider.image_for_rom(None))
