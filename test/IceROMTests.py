#!/usr/bin/env python
# encoding: utf-8
"""
IceROMTest.py

Created by Scott on 2012-12-26.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys, os
import unittest

from IceROM import ROM
from IceConsole import Console,console_lookup

class IceROMTests(unittest.TestCase):
    def setUp(self):
        gba = console_lookup("GBA")
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
        
    def test_executable(self):
        """
        The executable should be a file in the executables directory with the
        same name as the ROM. On Windows, this file should end with a .cmd file
        extension. On Mac/Linux systems, it should end with a .sh
        """
        rom_exe_location = self.rom.executable_path()
        # Assert that the exe is in the exe directory for it's console
        self.assertEqual(os.path.dirname(rom_exe_location),self.roms_console.executables_directory())
        # Assert that the exe name is the same as the ROM name with the correct
        # extension for the current platform
        if sys.platform.startswith('win'):
            self.assertEqual(os.path.basename(rom_exe_location),self.rom.name() + ".cmd")
        else:
            self.assertEqual(os.path.basename(rom_exe_location),self.rom.name() + ".sh")
    
	    