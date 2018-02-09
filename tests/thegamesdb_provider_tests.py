# encoding: utf-8
"""
consolegrid_provider_tests.py

Created by Wolfgang on 2018-02-09.
Copyright (c) 2018 Wolfgang Bergbauer. All rights reserved.
"""

import os
import unittest
from mockito import *
from urllib2 import URLError

# I need to do this instead of importing the class explicitly so that I can
# override the urllib2 function.
# TODO: Use dependency injection so I don't need to use that hack.
from ice.gridproviders import thegamesdb_provider


class TheGamesDBProviderTests(unittest.TestCase):

    def setUp(self):
        self.provider = thegamesdb_provider.TheGamesDBProvider()

    def tearDown(self):
        pass

    def create_mock_rom(self, rom_name="Test ROM", console_name="Test"):
        console = mock()
        console.fullname = console_name
        console.shortname = console_name

        rom = mock()
        rom.name = rom_name
        rom.console = console
        return rom

    def test_findId(self):
        rom = self.create_mock_rom("Mega Man")
        id = self.provider.findGamesDBId(rom)
        self.assertIsNotNone(id)

    def test_findArt(self):
        testid = 1093
        url = self.provider.findArtWorkUrl(testid)
        self.assertIsNotNone(url)

    def test_imageForRom(self):
        rom = self.create_mock_rom("Mega Man")
        image = self.provider.image_for_rom(rom)
        self.assertIsNotNone(image)