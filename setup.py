#!/usr/bin/env python
# encoding: utf-8
"""
setup.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

This code is heavily based off of code found at
http://www.py2exe.org/index.cgi/data_files

Thanks!
"""

import os
import glob

from distutils.core import setup

def find_data_files(source,target,patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
    return sorted(ret.items())

# Example:
setup(
    name="Ice",
    version="0.01",
    description="ROM Manager for Steam",
    author="Scott Rice",
    packages=["ice"],
    package_dir={'ice':'ice'},
    data_files=find_data_files('','',[
        'README.md',
        'resources/*',
    ])
)

# Will copy data/README to dist/README, and all files in data/images/ to dist/images/
# (not checking any subdirectories of data/images/)