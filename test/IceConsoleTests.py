#!/usr/bin/env python
# encoding: utf-8
"""
IceConsoleTests.py

Created by Scott on 2012-12-26.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys,os
import unittest

from ice import IceFilesystemHelper
from ice.IceConsole import Console, supported_consoles, console_lookup, gba

class IceConsoleTests(unittest.TestCase):
    def setUp(self):
        self.console = Console("Test","Test Console")
        
    def test_console_lookup(self):
        """
        Console lookup should do a few things:
        
        1) It should return the object from supported_consoles
        2) It should return the same instance every time
        3) It should return None when the console of that name is not found
        """
        # 1
        self.assertTrue(console_lookup("GBA") in supported_consoles)
        # 2
        self.assertEqual(console_lookup("GBA"),gba)
        self.assertEqual(console_lookup("GBA"),gba)
        # 3
        self.assertTrue(console_lookup("Random String") == None)
        
    # @unittest.skip("Not yet implemented")
    # def test_find_all_roms(self):
    #     pass
    # 
    # @unittest.skip("Not yet implemented")    
    # def test_find_all_roms_for_console(self):
    #     pass
        
    def test_roms_directory(self):
        """
        The ROMs directory for a console should be the ROMs directory from
        IceFilesystemHelper, except the directory name should be equal to the
        shortname for the console
        """
        gba_dir = self.console.roms_directory()
        self.assertEqual(os.path.dirname(gba_dir),IceFilesystemHelper.roms_directory())
        self.assertEqual(os.path.basename(gba_dir),self.console.shortname)
        
    def test_executables_directory(self):
        """
        The executables directory for a console should be a directory located
        in the main executables directory, and the consoles directory should be
        named the same as the shortname of the console
        """
        gba_dir = self.console.executables_directory()
        self.assertEqual(os.path.dirname(gba_dir),IceFilesystemHelper.executables_directory())
        self.assertEqual(os.path.basename(gba_dir),self.console.shortname)