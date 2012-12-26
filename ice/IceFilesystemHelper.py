#!/usr/bin/env python
# encoding: utf-8
"""
IceFilesystemHelper.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys
import os

import appdirs

import IceSettings

def roms_directory():
    """
    Should return a decent path in which to store ROMs. This path should be
    good for the user on any operating system. The path should be as follows
    on each OS...
    Windows XP: C:\Documents and Settings\Scott\My Documents\ROMs
    Windows 7: C:\Users\Scott\Documents\ROMs
    Mac OS X: /Users/scott/ROMs
    Linux: /home/scott/ROMs
    """
    return os.path.join(os.path.expanduser("~"),"ROMs")

def executables_directory():
    return os.path.join(appdirs.user_data_dir(IceSettings.appname,IceSettings.appauthor),"Exes")
    
def path_for_console(console):
    """
    Should return a directory with a decent name for each emulator, such as
    C:\Users\Scott\Documents\ROMs\N64
    or
    C:\Users\Scott\Documents\ROMs\PS2
    """
    return os.path.join(rom_directory(),console.shortname)

# def executable_path_for_shortcut(shortcut):
#     return os.path.join(executables_directory(),shortcut.appname+".cmd")