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

import platform

def windows_steam_is_running():
    """(Windows) Checks if Steam is currently running. Adapted from:
    http://timgolden.me.uk/python/wmi/cookbook.html"""
    return "Steam.exe" in subprocess.check_output("tasklist", shell=True)

def osx_steam_is_running():
    """(OS X) Checks if Steam is currently running."""
    return "Steam.app" in subprocess.check_output("ps -A", shell=True)

def linux_steam_is_running():
    """(Linux) Checks if Steam is currently running."""
    return "steam" in subprocess.check_output("ps -A", shell=True)

steam_is_running = platform.platform_specific(windows=windows_steam_is_running, osx=osx_steam_is_running, linux=linux_steam_is_running)