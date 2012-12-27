#!/usr/bin/env python
# encoding: utf-8
"""
IceROMTest.py

Created by Scott on 2012-12-26.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys
import unittest

from ice.IceROM import ROM
from ice.IceConsole import Console,console_lookup

class IceROMTests(unittest.TestCase):
    def setUp(self):
        gba = console_lookup("GBA")
        self.rom = ROM("/Users/scottrice/ROMs/GBA/Pokemon Emerald.gba",gba)
        self.noext_rom = ROM("/Users/scottrice/ROMs/GBA/Pokemon Emerald",gba)
    
    def test_name(self):
        # Name should be the name of the ROM file minus the extension
        self.assertEqual(self.rom.name(),"Pokemon Emerald")
        self.assertEqual(self.noext_rom.name(),"Pokemon Emerald")
        
    
	    