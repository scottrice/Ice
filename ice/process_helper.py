#!/usr/bin/env python
# encoding: utf-8
"""
process_helper.py

Created by Scott on 2013-06-03.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import subprocess

import settings

def windows_steam_is_running():
    """(Windows) Checks if Steam is currently running. Adapted from:
    http://timgolden.me.uk/python/wmi/cookbook.html"""
    return "Steam.exe" in subprocess.check_output("tasklist", shell=True)

def osx_steam_is_running():
    """(OS X) Checks if Steam is currently running."""
    return "Steam.app" in subprocess.check_output("ps -A", shell=True)

def linux_steam_is_running():
    """(Linux) Checks if Steam is currently running."""
    return False

# Sets 'steam_is_running' to be the correct method based on platform
platform = settings.platform_string()
if platform == "Windows":
    steam_is_running = windows_steam_is_running
elif platform == "OSX":
    steam_is_running = osx_steam_is_running
else:
    steam_is_running = linux_steam_is_running