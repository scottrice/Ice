#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Scott on 2012-12-26.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import unittest
from IceROMTests import IceROMTests
    
def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(IceROMTests)
    unittest.TextTestRunner().run(suite)