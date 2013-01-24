#!/usr/bin/env python
# encoding: utf-8
"""
IceLogging.py

Created by Scott on 2013-01-24.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import time

import IceFilesystemHelper

def log_timestamp_str():
    """
    Returns a nice string that represents the current time for use in logging
    
    Example:
    [1/24/2013 13:01:30]
    """
    time_str = time.strftime("%m/%d/%y %H:%M:%S")
    return "[%s]" % time_str

def log(s,level=1):
    """
    Logs the string s to a certain location, depending on the level.
    
    Level 0 is something that should be shown to the user immediately, normally
    printed to the console
    Level 1 is something that should be noted, but mainly for reference later.
    In the case of a level 1 log, the string should be put in a log file
    """
    if level == 0:
        print "%s %s" % (log_timestamp_str(),s)
    if level == 1:
        f = open(IceFilesystemHelper.log_file(),"a")
        f.write("%s %s\n" % (log_timestamp_str(),s))
        f.close()