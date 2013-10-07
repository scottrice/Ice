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
from emulators import custom_emulator
from ice_logging import log_file, log_both

# A map of "Emulator Name" => CustomEmulator object
cached_emulators = None
def custom_emulators():
    global cached_emulators
    if cached_emulators is None:
        cached_emulators = {}
        emulator_data = settings.emulators()
        for name in emulator_data.keys():
            current = emulator_data[name]
            if 'location' not in current or current['location'] == "":
                log_both("No location set for '%s' in emulators.txt. Ignoring emulator" % name)
                continue
            if 'command' not in current or current['command'] == "":
                log_both("No command set for '%s' in emulators.txt. Ignoring emulator" % name)
                continue
            current_emulator = custom_emulator.CustomEmulator(name, current['location'], current['command'])
            cached_emulators[name] = current_emulator
    return cached_emulators

def lookup_emulator(console):
    try:
        emulator_name = settings.consoles()[console.fullname]['emulator']
    except KeyError as e:
        log_file("No emulator supplied for %s" % (console.shortname))
        return None
    if emulator_name not in custom_emulators():
        log_file("Emulator '%s' not found for %s. Ignoring" % (emulator_name, console.fullname))
        return None
    return custom_emulators()[emulator_name]