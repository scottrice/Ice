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

import urllib
import urllib2
import urlparse
import steam_user_manager
import steam_grid
import settings
from ice_logging import ice_logger
from error.config_error import ConfigError

# Providers
from gridproviders import local_provider
from gridproviders import consolegrid_provider

class IceGridImageManager():
    
    def __init__(self):
        self.providers = [
            local_provider.LocalProvider(),
            consolegrid_provider.ConsoleGridProvider(),
        ]
    
    def image_for_rom(self, rom):
        """
        Goes through each provider until one successfully finds an image.
        Returns None if no provider was able to find an image
        """
        for provider in self.providers:
            (path, error) = provider.image_for_rom(rom)
            if path is not None:
                return path
            # TODO: Log the error for the provider
            # ice_logger.error(error)
        return None

    def update_user_images(self, user_id, roms):
        """
        Sets a suitable grid image for every rom in 'roms' for the user
        defined by 'user_id'
        """
        grid = steam_grid.SteamGrid(steam_user_manager.userdata_directory_for_user_id(user_id))
        for rom in roms:
            shortcut = rom.to_shortcut()
            if not grid.existing_image_for_filename(grid.filename_for_shortcut(shortcut.appname, shortcut.exe)):
                path = self.image_for_rom(rom)
                if path is None:
                    # TODO: Tell the user what went wrong
                    pass
                else:
                    # TODO: Tell the user that an image was found
                    ice_logger.log("Found grid image for %s" % shortcut.appname)
                    grid.set_image_for_shortcut(path, shortcut.appname, shortcut.exe)
