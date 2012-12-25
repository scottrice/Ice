#!/usr/bin/env python
"""
SteamInstallationLocationManager.py

Created by Scott on 2012-12-20.
Copyright (c) 2012 Scott Rice. All rights reserved.

The purpose of this class is to abstract away finding/storing the install
location of Steam. A corrolary of this is that it should be easy to find the
shortcuts.vdf file, which is obviously useful for Ice
"""

import sys
import os

import SteamUserManager

# As of right now, I'm not sure why I will need this, but I think it will be useful
default_steam_directory = {}
default_steam_directory["windows"] = "C:\Program Files (x86)\Steam\\"
default_steam_directory["osx"] = "/Applications/Steam.app/Contents/MacOS/"

# Used to find the shortcuts.vdf file
default_userdata_directory = {}
default_userdata_directory["windows"] = "C:\Program Files (x86)\Steam\userdata\\"
default_userdata_directory["osx"] = "~/Library/Application Support/Steam/userdata/"

# TODO: Check if the default location exists. If it doesn't, search the filesystem to find it.
# TODO: Generate based on operating system
def steam_location():
    return default_steam_directory["osx"]

# TODO: Check if the default location exists. If it doesn't, search the filesystem to find it.
# TODO: Generate based on operating system
def steam_userdata_location():
    return default_userdata_directory["osx"]