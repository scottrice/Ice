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

# Used to find the shortcuts.vdf file
osx_userdata_directory = "~/Library/Application Support/Steam/userdata/"

def steam_location():
    location = settings.config()["Steam"]["location"]
    if not os.path.exists(os.path.join(location,"Steam.exe")):
        raise StandardError("Steam not found at specified location. Make sure that the Steam Location in config.txt is set to the directory containing your Steam installation")
    return settings.config()["Steam"]["location"]

def steam_userdata_location():
    platform = settings.platform_string()
    if platform == "Windows":
        # On Windows, the userdata directory is the steam installation directory
        # with 'userdata' appeneded
        return os.path.join(steam_location(),"userdata")
    elif platform == "OSX":
        # I'm pretty sure the user can't change this on OS X. I think it always
        # goes to the same location
        return os.path.expanduser(osx_userdata_directory)