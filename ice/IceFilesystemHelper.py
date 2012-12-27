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
    """
    Should return a decent path in which to store executables. This path should
    be out of the way for users on every Operating System (executables needed
    by Steam are an implementation detail that users shouldn't have to worry 
    about)
    
    Example...
    Windows: C:\Users\<username>\AppData\Local\Scott Rice\Ice\Exes
    Max OS X: ~/Library/Application Support/Ice/Exes
    
    """
    return os.path.join(appdirs.user_data_dir(IceSettings.appname,IceSettings.appauthor),"Exes")
    
def cache_directory():
    """
    Returns the path to a directory where Ice can store persistant data without
    worry of user interference
    
    Example...
    Windows: C:\Users\<username>\AppData\Local\Scott Rice\Ice\_cache
    Max OS X: ~/Library/Application Support/Ice/_cache
    """
    return os.path.join(appdirs.user_data_dir(IceSettings.appname,IceSettings.appauthor),"_cache")    
    
def cache_file(filename):
    """
    Returns the path to a file in the caches directory such that Ice can easily
    save/store persistant data for the next run
    """
    # TODO: Automatically save cache files when python exits, so I can write to
    # these files without worrying about having to save when I am done
    return os.path.join(cache_directory(),filename)