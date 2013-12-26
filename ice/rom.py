#!/usr/bin/env python
# encoding: utf-8
"""
IceROM.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

ROM model. Handles the collection of data that makes up a ROM (as of right now,
just the path to the ROM and what console is is from). Also contains some
convenience methods for the filesystem. 

Functionality should be added to this class if it heavily involves the use of
ROMs
"""

import sys
import os
import stat
import unicodedata

import platform_helper as pf
from steam_shortcut_manager import SteamShortcut

class ROM:
    def __init__(self,path,console):
        self.path = path
        self.console = console

    def __repr__(self):
        return self.name()

    def __eq__(self,other):
        return self.path == other.path and self.console == other.console
        
    def basename(self):
        name_with_ext = os.path.basename(self.path)

        # normalize the name to get rid of symbols that break the shortcuts.vdf
        name_with_ext = unicodedata.normalize('NFKD', unicode(name_with_ext.decode('utf-8'))).encode('ascii', 'ignore')

        dot_index = name_with_ext.rfind('.')
        if dot_index == -1:
            # There is no period, so there is no extension. Therefore, the
            # name with extension is the name
            return name_with_ext
        # Return the entire string leading up to (but not including) the period
        return name_with_ext[:dot_index]

    def name(self):
        prefix = self.console.prefix
        if prefix:
            return "%s %s" % (prefix, self.basename())
        else:
            return self.basename()
        
    def to_shortcut(self):
        command_string = self.console.emulator.command_string(self)
        startdir = self.console.emulator.startdir(self)
        return SteamShortcut(self.name(),command_string,startdir,self.console.icon,self.console.fullname)
