#!/usr/bin/env python
# encoding: utf-8
"""
setup.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

I have no idea what I'm doing...
"""

import os
import sys
import glob

from setuptools import setup, find_packages

if sys.platform.startswith("win"):
  import py2exe

# py2exe options. The tutorial I used is here:
# http://www.blog.pythonlibrary.org/2010/07/31/a-py2exe-tutorial-build-a-binary-series/
includes = []
excludes = []
packages = ["ice","ice.emulators","ice.resources","ice.resources.images","ice.resources.images.icons"]
# packages = []
dll_excludes = []

SRC_DIR = 'ice'

setup(
    name="Ice",
    version="0.01",
    description="ROM Manager for Steam",
    author="Scott Rice",
    console=["ice.py"],
    include_package_data=True,
    # package_dir={'':'.'},
    packages=packages,
    package_data={'ice':['resources/images/icons/*']},
    options = {"py2exe": {"compressed": 2, 
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },
)

# Will copy data/README to dist/README, and all files in data/images/ to dist/images/
# (not checking any subdirectories of data/images/)