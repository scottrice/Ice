#!/usr/bin/env python
# encoding: utf-8
"""
filesystem_helper.py

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

import os

import appdirs

import settings
from error.config_error import ConfigError
from ice_logging import log_both

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

def create_directory_if_needed(dir, log=None):
    """
    Checks to see if a directory exists and, if not, creates it
    """
    if not os.path.exists(dir):
        if log is not None:
            log_both(log)
        os.makedirs(dir)


def assert_file_exists(path, exception=None):
    if not os.path.isfile(path):
        raise exception

def roms_directory():
    """
    Returns the path to the ROMs directory, as specified by config.txt.
    """
    path = os.path.expanduser(settings.config()['Storage']['roms directory'])
    if path == "":
        path = os.path.join(os.path.expanduser("~"), "ROMs")
    if os.path.exists(path) and not os.access(path, os.W_OK):
        fix_instructions = "Ice does not have permission to write to your ROMs Directory, %s. Please choose a different folder or change your permissions." % path
        raise ConfigError("Storage","ROMs Directory", fix_instructions)
    return path

def log_file():
    """
    Should return the path for the log file. The log file should be located in
    the app's data directory and should be called 'log.txt'
    
    Example...
    Windows: C:\Users\<username>\AppData\Local\Scott Rice\Ice\log.txt
    Max OS X: ~/Library/Application Support/Ice/log.txt
    """
    return os.path.join(app_data_directory(),"log.txt")
