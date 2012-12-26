#!/usr/bin/env python
# encoding: utf-8
"""
IceROM.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys
import os

import IceFilesystemHelper

class ROM:
    def __init__(self,path,console):
        self.path = path
        self.console = console
        
    def name(self):
        name_with_ext = os.path.basename(self.path)
        dot_index = name_with_ext.rfind('.')
        if dot_index == -1:
            # There is no period, so there is no extension. Therefore, the
            # name with extension is the name
            return name_with_ext
        # Return the entire string leading up to (but not including) the period
        return name_with_ext[:dot_index]
        
    def executable(self):
        return os.path.join(self.console.executables_directory(),self.name()+".cmd")