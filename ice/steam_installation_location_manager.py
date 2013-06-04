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

from error.config_error import ConfigError

# Used to find the shortcuts.vdf file
osx_userdata_directory = "~/Library/Application Support/Steam/userdata/"

def windows_steam_location():
    import _winreg as registry
    key = registry.CreateKey(registry.HKEY_CURRENT_USER,"Software\Valve\Steam")
    return registry.QueryValueEx(key,"SteamPath")[0]

def steam_userdata_location():
    platform = settings.platform_string()
    if platform == "Windows":
        # On Windows, the userdata directory is the steam installation directory
        # with 'userdata' appeneded
        return os.path.join(windows_steam_location(),"userdata")
    elif platform == "OSX":
        # I'm pretty sure the user can't change this on OS X. I think it always
        # goes to the same location
        return os.path.expanduser(osx_userdata_directory)