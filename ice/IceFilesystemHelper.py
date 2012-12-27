#!/usr/bin/env python
# encoding: utf-8
"""
IceFilesystemHelper.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

Abstracts away filesystem specific information into app-specific methods. For
example, the app doesn't care about where exactly on the filesystem the ROMs
directory is located, it just wants to know what ROMs are a part of it. This
module is meant to deal with that abstraction.

Functionality should be added to this module if it involves the filesystem, but
doesn't heavily involve any of the other datatypes used by this app (Consoles,
ROMs, etc)
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