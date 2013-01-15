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

def create_directory_if_needed(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def app_data_directory():
    """
    Should return a decent path for Ice to store any kind of settings/data it
    needs. One example of this would be the exes directory.
    
    Example...
    Windows: C:\Users\<username>\AppData\Local\Scott Rice\Ice\\
    Mac OS X: ~/Library/Application Support/Ice/
    """
    return appdirs.user_data_dir(IceSettings.appname,IceSettings.appauthor)

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
    return os.path.join(app_data_directory(),"Exes")

def resources_directory():
    """
    Should return the path to the resources directory in our package
    """
    this_dir, this_filename = os.path.split(__file__)
    return os.path.join(this_dir,"resources")
    
def icons_directory():
    """
    Should return the path for the icons directory
    """
    return os.path.join(resources_directory(),"images","icons")
    
def bundled_emulators_directory(platform):
    """
    Should return the path for the emulators directory in the package for a
    given platform
    """
    return os.path.join(resources_directory(), "emulators",platform)

def downloaded_emulators_directory():
    """
    Should return the path for a directory suitable to store downloaded 
    emulators. This will be in the app data directory, in a folder called
    'Emulators'
    
    Example...
    Windows: C:\Users\<username>\AppData\Local\Scott Rice\Ice\Emulators
    Max OS X: ~/Library/Application Support/Ice/Emulators
    """
    return os.path.join(app_data_directory(),"Emulators")
    
def downloaded_zips_directory():
    """
    Should return the path for a directory suitable to store downloaded 
    zip files (so we know if we have downloaded a zip before). This will be in
    the app data directory, in a folder called 'Downloaded Zips'
    
    Example...
    Windows: C:\Users\<username>\AppData\Local\Scott Rice\Ice\Downloaded Zips
    Max OS X: ~/Library/Application Support/Ice/Downloaded Zips
    """
    return os.path.join(app_data_directory(),"Downloaded Zips")

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