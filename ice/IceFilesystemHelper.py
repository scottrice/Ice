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

def highest_directory_in_path(path):
    """
    Returns the 'highest' directory in a path, which is defined as the first
    path component
    
    Example In => Out
    (Mac)
    /Users/scottrice/Documents/Resume.pdf => /
    Users/scottrice/Documents/Resume.pdf => Users
    (Windows)
    C:\\Users\Scott\Documents\Resume.pdf => C:\
    bsnes\\bsnes.exe => bsnes
    """
    # We don't support absolute paths because of how os.path.split handles the
    # path = "/" case
    if path.startswith("/"):
        return "/"
    (head,tail) = os.path.split(path)
    # Empty string is falsy, so this is checking for "if head is not empty"
    if head:
        return highest_directory_in_path(head)
    else:
        return tail

def create_directory_if_needed(dir):
    """
    Checks to see if a directory exists and, if not, creates it
    """
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

def log_file():
    """
    Should return the path for the log file. The log file should be located in
    the app's data directory and should be called 'log.txt'
    
    Example...
    Windows: C:\Users\<username>\AppData\Local\Scott Rice\Ice\log.txt
    Max OS X: ~/Library/Application Support/Ice/log.txt
    """
    return os.path.join(app_data_directory(),"log.txt")