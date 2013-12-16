#!/usr/bin/env python
"""
steam_installation_location_manager.py

Created by Scott on 2012-12-20.
Copyright (c) 2012 Scott Rice. All rights reserved.

The purpose of this class is to abstract away finding/storing the install
location of Steam. A corrolary of this is that it should be easy to find the
shortcuts.vdf file, which is obviously useful for Ice
"""

import os

import platform_helper as pf
import settings

# Used to find the shortcuts.vdf file
osx_userdata_directory = "~/Library/Application Support/Steam/userdata/"
linux_userdata_directory = "~/.local/share/Steam/userdata/"

def config_userdata_location():
    return os.path.expanduser(settings.config()["Steam"]["userdata directory"])

def windows_steam_location():
    import _winreg as registry
    key = registry.CreateKey(registry.HKEY_CURRENT_USER,"Software\Valve\Steam")
    return registry.QueryValueEx(key,"SteamPath")[0]

def windows_userdata_location():
    # On Windows, the userdata directory is the steam installation directory
    # with 'userdata' appended
    if config_userdata_location() == "":
        try:
            out = os.path.join(windows_steam_location(),"userdata")
        except WindowsError:
            raise IOError("Steam installation not found\n"
                          "Please reinstall Steam or configure its userdata directory in config.txt")
    else:
        out = config_userdata_location()
    return out

def osx_userdata_location():
    # I'm pretty sure the user can't change this on OS X. I think it always
    # goes to the same location
    if config_userdata_location() == "":
        out = os.path.expanduser(osx_userdata_directory)
    else:
        out = config_userdata_location()
    if not os.path.exists(out):
        raise IOError("Steam userdata directory not found in location:\n" + out +
                      "\nPlease configure Steam's userdata directory in config.txt")
    return out

def linux_userdata_location():
    if config_userdata_location() == "":
        out = os.path.expanduser(linux_userdata_directory)
    else:
        out = config_userdata_location()
    if not os.path.exists(out):
        raise IOError("Steam userdata directory not found in location:\n" + out +
                      "\nPlease configure Steam's userdata directory in config.txt")
    return out

steam_userdata_location = pf.platform_specific(windows=windows_userdata_location, osx=osx_userdata_location, linux=linux_userdata_location)
