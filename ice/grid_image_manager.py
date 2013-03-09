#!/usr/bin/env python
# encoding: utf-8
"""
IceGridImageManager.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

The purpose of this class is to handle the downloading and setting of Steam
App Grid images for each shortcut.

Functionality should be added to this class if it involves Steam App Grid 
images.
"""

import os
import sys
import steam_user_manager
import steam_grid
from ice_logging import log

class IceGridImageManager():
    def __init__(self):
        pass
        
    def find_image_for_rom(self,rom):
        """
        Determines a suitable grid image for a given ROM.
        """
        # Right now this method can't find any games, but if you give it a path
        # you will see Ice set that image for all of your games.
        #
        # TODO: Make this method find images online
        return None
        
    def update_user_images(self,user_id,roms):
        """
        Sets a suitable grid image for every rom in 'roms' for the user defined
        by 'user_id'
        """
        grid = steam_grid.SteamGrid(steam_user_manager.userdata_directory_for_user_id(user_id))
        for rom in roms:
            shortcut = rom.to_shortcut()
            if not grid.existing_image_for_filename(grid.filename_for_shortcut(shortcut.appname,shortcut.exe)):
                image = self.find_image_for_rom(rom)
                if image:
                    log("Setting custom image for %s" % rom.name(),1)
                    grid.set_image_for_shortcut(self.find_image_for_rom(rom),shortcut.appname,shortcut.exe)
                else:
                    log("No image found for %s on %s" % (rom.name(),rom.console.fullname))
                    log("We couldn't find an image for %s. If you find one you like, upload it to something.com, and next time Ice runs it will use it" % rom.name(),2)