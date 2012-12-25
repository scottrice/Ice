#!/usr/bin/env python

import sys
import os

import SteamShortcutManager.SteamShortcutManager
import SteamInstallationLocationManager
import SteamUserManager
import IceFilesystemHelper

# print SteamUserManager.name_from_communityid64(76561198000852103)
# print "------------------------"
# print SteamUserManager.communityid64_from_name("meris608")
# print "------------------------"
# print SteamUserManager.communityid32_from_name("meris608")
# print "------------------------"
# print SteamUserManager.userdata_directory_for_user_id("40586375")
# print "------------------------"
print IceFilesystemHelper.executables_directory()

def main():
    # Find the Steam Account that the user would like to add ROMs for
    # Parse their shortcuts.vdf into a Shortcut Manager object
    # Find all of the ROMs that are currently in the designated folders
    # Add the new ROMs in each folder to our Shortcut Manager
    # Generate a new shortcuts.vdf file with all of the new additions
    print "Hi!"
    
if __name__ == "__main__":
    main()