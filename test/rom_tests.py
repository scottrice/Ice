#!/usr/bin/env python
# encoding: utf-8
"""
rom_test.py

Created by Scott on 2012-12-26.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys
import os
import unittest

from rom import ROM
from console import Console


class ROMTests(unittest.TestCase):
    def setUp(self):
        gba = Console("GBA", "Gameboy Advance")
        self.roms_console = gba
        self.rom = ROM("/Users/scottrice/ROMs/GBA/Pokemon Emerald.gba",gba)
        self.noext_rom = ROM("/Users/scottrice/ROMs/GBA/Pokemon Emerald",gba)
    
    def test_name(self):
        """
        Name should be the name of the ROM file minus the extension.
        If the ROM has no extension, then the name should just be the name of
        the ROM file
        """
        self.assertEqual(self.rom.name(),"Pokemon Emerald")
        self.assertEqual(self.noext_rom.name(),"Pokemon Emerald")
