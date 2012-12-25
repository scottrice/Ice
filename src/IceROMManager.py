#!/usr/bin/env python
# encoding: utf-8
"""
IceROMManager.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys
import os

import IceFilesystemHelper

# Check to see if the directory we are going to use to Store ROMs exists. If it
# does not, then create it.
if not os.path.exists(IceFilesystemHelper.roms_directory()):
    os.makedirs(IceFilesystemHelper.roms_directory())

