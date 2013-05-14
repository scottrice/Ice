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
import traceback

import filesystem_helper

def log_timestamp_str():
    """
    Returns a nice string that represents the current time for use in logging
    
    Example:
    [1/24/2013 13:01:30]
    """
    time_str = time.strftime("%m/%d/%y %H:%M:%S")
    return "[%s]" % time_str

# def log(s,level=1):
#     """
#     Logs the string s to a certain location, depending on the level.
#     
#     Level 0 is something that should be shown to the user immediately, normally
#     printed to the console
#     Level 1 is something that should be noted, but mainly for reference later.
#     In the case of a level 1 log, the string should be put in a log file
# 
#     If 'level' is 2, then both print the message and make note in the file
#     """
#     if level is 0 or level is 2:
#         print "%s" % s
#     if level is 1 or level is 2:
#         f = open(filesystem_helper.log_file(),"a")
#         f.write("%s %s\n" % (log_timestamp_str(),s))
#         f.close()
        
def log_user(s):
    """
    Logs the string s to the user
    """
    print s
    
def log_file(s):
    """
    Logs the string s in a file, defined in filesystem_helper
    """
    f = open(filesystem_helper.log_file(),"a")
    f.write("%s %s\n" % (log_timestamp_str(),s))
    f.close()
    
def log_both(s):
    """
    Logs the string s to both the user and to a file
    """
    log_user(s)
    log_file(s)
    
def log_exception():
    traceback.print_exc(file=open(filesystem_helper.log_file(),"a"))