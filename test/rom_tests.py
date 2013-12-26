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

    def test_basename(self):
        """
        Basename should be the name of the ROM file minus the extension.
        If the ROM has no extension, then the name should just be the name of
        the ROM file
        """
        gba = Console("Gameboy Advance")
        prefix_gba = Console("Gameboy Advance", { "prefix":"Any Text" })
        rom_path = "/Users/scottrice/ROMs/GBA/Pokemon Emerald.gba"
        noext_rom_path = "/Users/scottrice/ROMs/GBA/Pokemon Emerald"
        rom = ROM(rom_path,gba)
        noext_rom = ROM(noext_rom_path,gba)
        prefix_rom = ROM(rom_path, prefix_gba)

        # Standard situation
        self.assertEqual(rom.basename(),"Pokemon Emerald")
        # Should correctly figure out the basename when the ROM has no extension
        self.assertEqual(noext_rom.basename(),"Pokemon Emerald")
        # The basename shouldn't include the prefix
        self.assertEqual(prefix_rom.basename(), "Pokemon Emerald")

    def test_name(self):
        prefix = "Any Text"
        gba = Console("Gameboy Advance")
        prefix_gba = Console("Gameboy Advance", { "prefix": prefix })
        empty_prefix_gba = Console("Gameboy Advance", {"prefix": "" })
        rom_path = "/Users/scottrice/ROMs/GBA/Pokemon Emerald.gba"

        rom = ROM(rom_path, gba)
        prefix_rom = ROM(rom_path, prefix_gba)
        empty_prefix_rom = ROM(rom_path, empty_prefix_gba)

        # With no prefix, the name should be the same as the basename
        self.assertEqual(rom.name(), "Pokemon Emerald")
        # When the prefix is the empty string, it should be treated as if no
        # prefix was given
        self.assertEqual(empty_prefix_rom.name(), "Pokemon Emerald")
        # When the console has a prefix, the ROM should begin with that string
        self.assertTrue(prefix_rom.name().startswith(prefix))
