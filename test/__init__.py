#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Scott on 2012-12-26.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import os
import sys
import unittest


#
# The code below is based off of gorakhargosh's watchdog, which is graciously
# provided at https://github.com/gorakhargosh/watchdog. It is licensed under
# the Apache License, which you can find here:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
current_path = os.path.abspath(os.path.dirname(__file__))
tests_path = os.path.join(current_path)
sys.path[0:0] = [
  current_path,
  tests_path,
]

all_tests = [f[:-3] for f in os.listdir(tests_path)
             if f.endswith("tests.py")]

def get_suite(tests):
  tests = sorted(tests)
  suite = unittest.TestSuite()
  loader = unittest.TestLoader()
  for test in tests:
    suite.addTest(loader.loadTestsFromName(test))
  return suite
  
def run_tests():
  tests = sys.argv[1:]
  if not tests:
    tests = all_tests
  tests = ['%s' % t for t in tests]
  suite = get_suite(tests)
  unittest.TextTestRunner(verbosity=2).run(suite)