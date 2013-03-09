#!/usr/bin/env python
# encoding: utf-8
"""
bundled_emulator.py

Created by Scott on 2013-01-05.
Copyright (c) 2013 Scott Rice. All rights reserved.

BundledEmulator represents an emulator which comes packaged with Ice in it's
resources directory.

Functionality should be added here if it involves only emulators which have
been bundled
"""

import sys
import os
import abc

from ice import filesystem_helper

import emulator

class BundledEmulator(emulator.Emulator):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self,console_name,emulator_location):
        super(BundledEmulator,self).__init__(console_name)
        assert self._relative_exe_path_, "Relative Exe Path must be defined for all subclasses of BundledEmulator"
        self.location = os.path.join(filesystem_helper.bundled_emulators_directory(),self._relative_exe_path_)