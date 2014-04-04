#!/usr/bin/env python
# encoding: utf-8
"""
process_helper.py

Created by Scott on 2013-06-03.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import subprocess

import platform_helper as pf
from ice_logging import ice_logger

def windows_steam_is_running():
    """(Windows) Checks if Steam is currently running."""
    return "Steam.exe" in subprocess.check_output("tasklist", shell=True)

def osx_steam_is_running():
    """(OS X) Checks if Steam is currently running."""
    return "Steam.app" in subprocess.check_output("ps -A", shell=True)

def linux_steam_is_running():
    """(Linux) Checks if Steam is currently running."""
    return "steam" in subprocess.check_output("ps -A", shell=True)

def steam_is_running():
  check_function = pf.platform_specific(windows=windows_steam_is_running, osx=osx_steam_is_running, linux=linux_steam_is_running)
  try:
    return check_function()
  except:
    ice_logger.log_warning('Could not determine if Steam is running. Make sure Steam is closed before running Ice.')
    return False