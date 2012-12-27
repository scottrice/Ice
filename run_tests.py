#!/usr/bin/env python
# encoding: utf-8
"""
run_tests.py

Created by Scott on 2012-12-26.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys, os, inspect
from test import run_tests

# The code below is to allow test cases to import the class they are testing by
# using the syntax 'import ice.******'.
#
# This code was taken from a StackOverflow answer by sorin. The internet is
# down right now but I will link to it when I get the chance.
#
# Get a reference to the current directory, without using __file__, which fails
# in certain situations based on how you call the script in Windows
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0,cmd_folder)

run_tests()