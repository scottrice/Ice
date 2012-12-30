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
# TODO: Find out the default install location of Steam on Linux
default_steam_directory["linux"] = ""

# Used to find the shortcuts.vdf file
default_userdata_directory = {}
default_userdata_directory["windows"] = "C:\Program Files (x86)\Steam\userdata\\"
default_userdata_directory["osx"] = "~/Library/Application Support/Steam/userdata/"
# TODO: Find out the default userdata directory on Linux
default_steam_directory["linux"] = ""

# TODO: Check if the default location exists. If it doesn't, search the filesystem to find it.
def steam_location():
    if sys.platform.startswith('win'):
        return default_steam_directory["windows"]
    elif sys.platform.startswith('darwin'):
        return os.path.expanduser(default_steam_directory["osx"])
    return default_steam_directory["linux"]

# TODO: Check if the default location exists. If it doesn't, search the filesystem to find it.
def steam_userdata_location():
    if sys.platform.startswith('win'):
        return default_userdata_directory["windows"]
    elif sys.platform.startswith('darwin'):
        return os.path.expanduser(default_userdata_directory["osx"])
    return default_userdata_directory["linux"]