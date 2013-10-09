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
from ice_logging import log_user,log_file,log_both
from error.config_error import ConfigError

class IceGridImageManager():
    @staticmethod
    def should_download_images():
        try:
            should_download = settings.config()["Grid Images"]["source"] != ""
            return should_download
        except KeyError:
            log_both("Could not find '[Grid Images] Source' in config.txt.")
            return False

    def __init__(self):
        pass
    
    def provider_with_protocol(self):
        host = settings.config()["Grid Images"]["source"]
        if not host.startswith("http://"):
          host = "http://" + host
        return host
    
    def host_for_image_source(self):
        return urlparse.urlparse(self.provider_with_protocol()).hostname
        
    def url_for_rom(self,rom):
        host = self.provider_with_protocol()
        quoted_name = urllib.quote(rom.name())
        return "%s?console=%s&game=%s" % (host,rom.console.shortname,quoted_name)
        
    def find_image_for_rom(self,rom):
        """
        Determines a suitable grid image for a given ROM.
        """
        try:
            response = urllib2.urlopen(self.url_for_rom(rom))
            if response.getcode() == 204:
              return None
            else:
              return response.read()
        except urllib2.URLError as error:
            # Connection was refused. The config was incorrect. Let the user
            # know to change it
            raise ConfigError("Grid Images", "Source", "The source of game images is unavailable.")
          
    def download_image(self,image_url):
        """
        Downloads the image at 'image_url' and returns the path to the image on
        the local filesystem
        """
        (path,headers) = urllib.urlretrieve(image_url)
        return path
        
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
                # Game not found
                if image is None:
                    log_file("No game found for %s on %s" % (rom.name(),rom.console.fullname))
                    log_user("The image provider has no game called %s for %s. Try going to %s and submittng the game yourself" % (rom.name(),rom.console.fullname, self.host_for_image_source()))
                # Game found, but there is no picture
                elif image == "":
                    log_file("No image found for %s. The URL checked was '%s'" % (rom.name(),self.url_for_rom(rom)))
                    log_user("We couldn't find an image for %s. If you find one you like, upload it to %s, and next time Ice runs it will use it" % (rom.name(),self.host_for_image_source()))
                # Game found, AND there is a picture there
                else:
                    log_file("Setting custom image for %s" % rom.name())
                    image_path = self.download_image(image)
                    grid.set_image_for_shortcut(image_path,shortcut.appname,shortcut.exe)