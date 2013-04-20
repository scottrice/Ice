#!/usr/bin/env python
"""
steam_installation_location_manager.py

Created by Scott on 2012-12-20.
Copyright (c) 2012 Scott Rice. All rights reserved.

The purpose of this class is to abstract away finding/storing the install
location of Steam. A corrolary of this is that it should be easy to find the
shortcuts.vdf file, which is obviously useful for Ice
"""

import sys
import os

import settings

# TODO: Removed what I think is an unused import, but it is very possible that I
# will be getting a bunch of errors pretty soon, so just putting this TODO here
# to remind me

# As of right now, I'm not sure why I will need this, but I think it will be useful
default_steam_directory = {}
default_steam_directory["Windows"] = "C:\Program Files (x86)\Steam\\"
default_steam_directory["OSX"] = "/Applications/Steam.app/Contents/MacOS/"
# TODO: Find out the default install location of Steam on Linux
default_steam_directory["Linux"] = ""

# Used to find the shortcuts.vdf file
default_userdata_directory = {}
default_userdata_directory["Windows"] = "C:\Program Files (x86)\Steam\userdata\\"
default_userdata_directory["OSX"] = "~/Library/Application Support/Steam/userdata/"
# TODO: Find out the default userdata directory on Linux
default_steam_directory["Linux"] = ""

# TODO: Check if the default location exists. If it doesn't, search the filesystem to find it.
def steam_location():
    platform = settings.platform_string()
    return os.path.expanduser(default_steam_directory[platform])

def steam_userdata_location():
    platform = settings.platform_string()
    if platform == "Windows":
        # On Windows, the userdata directory is the steam installation directory
        # with 'userdata' appeneded
        return os.path.join(steam_location(),"userdata")
    elif platform == "OSX":
        # I'm pretty sure the user can't change this on OS X. I think it always
        # goes to the same location
        return os.path.expanduser(default_userdata_directory["osx"])