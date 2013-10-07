#!/usr/bin/env python
# encoding: utf-8
"""
emulator_manager.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import settings

import platform
from emulators import *
from error.config_error import ConfigError
from ice_logging import log_file, log_user

def windows_prefix():
    return "Win"

def mac_prefix():
    return "Mac"

def linux_prefix():
    return "Lin"

emulator_platform_prefix = platform.platform_specific(windows=windows_prefix, osx=mac_prefix, linux=linux_prefix)

def emulator_from_name(emulator_name):
    """Grabs the emulator subclass described by 'emulator_name'. This function
    assumes that an emulator named 'WinProject64' will be in a module called
    'winproject64'."""
    return getattr(globals()[emulator_name.lower()], emulator_name)

def lookup_emulator(console):
    try:
        user_supplied_name = settings.consoles()[console.fullname]['emulator']
    except KeyError as e:
        log_file("No emulator supplied for %s" % (console.shortname))
        return None

    if not user_supplied_name:
        log_file("No user supplied name for %s" % console.shortname)
        return None

    name = emulator_platform_prefix() + user_supplied_name
    try:
        return emulator_from_name(name)(console.shortname)
    except (KeyError, AttributeError) as e:
        message = "Could not load emulator. Check your spelling, and make sure the emulator is supported for your console"
        raise ConfigError(console.fullname, 'emulator', message, file="consoles.txt")
