#!/usr/bin/env python
# encoding: utf-8
"""
console_tests.py

Created by Scott on 2012-12-26.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import os
import unittest

import filesystem_helper
from console import Console, supported_consoles

class ConsoleTests(unittest.TestCase):
    def setUp(self):
        self.console = Console("Test","Test Console")
        
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
        filesystem_helper, except the directory name should be equal to the
        shortname for the console
        """
        gba_dir = self.console.roms_directory()
        self.assertEqual(os.path.dirname(gba_dir),filesystem_helper.roms_directory())
        self.assertEqual(os.path.basename(gba_dir),self.console.shortname)
        
    def test_executables_directory(self):
        """
        The executables directory for a console should be a directory located
        in the main executables directory, and the consoles directory should be
        named the same as the shortname of the console
        """
        gba_dir = self.console.executables_directory()
        self.assertEqual(os.path.dirname(gba_dir),filesystem_helper.executables_directory())
        self.assertEqual(os.path.basename(gba_dir),self.console.shortname)
        
    def test_icon_path(self):
        """
        The icon path for a console should be in the icons directory, and the
        file should be named the shortname of the console with a .png extension
        """
        gba_path = self.console.icon_path()
        self.assertEqual(os.path.dirname(gba_path),filesystem_helper.icons_directory())
        self.assertEqual(os.path.basename(gba_path),self.console.shortname + ".png")