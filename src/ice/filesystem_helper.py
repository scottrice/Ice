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

from ice_logging import ice_logger

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
            ice_logger.log(log)
        os.makedirs(dir)

def assert_file_exists(path, exception=None):
    if not os.path.isfile(path):
        raise exception

def available_to_use(path, create_if_needed=False):
    """
    Checks a boolean based on whether a directory is 'available' for Ice to use.
    This means that not only does the path exist, but Ice has write access to it
    as well.

    When create_if_needed is set to True, Ice will attempt to create a directory
    if one does not exist at path. Any errors in this operation will be logged
    to the log file and this function will return False
    """
    # Ensure the directory exists
    try:
        if create_if_needed:
            create_directory_if_needed(path, log="Creating directory at %s" % path)
        # Ensure that it worked
        if not os.path.exists(path):
            return False
    # Might not be necessary, but in case create_directory_if_needed fails...
    except:
        return False

    # Check that we have write access to the directory
    if not os.access(path, os.W_OK):
        return False

    # Woohoo!
    return True
