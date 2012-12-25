#!/usr/bin/env python
# encoding: utf-8
"""
IceConsole.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys
import os

import IceFilesystemHelper

class Console():
    def __init__(self,shortname,fullname,emulator):
        self.shortname = shortname
        self.fullname = fullname
        self.emulator = emulator
        
    def path(self):
        return IceFilesystemHelper.path_for_console(self)

n64 = Console("N64","Nintendo 64",)

supported_consoles = [
    
]