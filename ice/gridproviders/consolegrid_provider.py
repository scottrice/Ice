#!/usr/bin/env python
# encoding: utf-8
"""
consolegrid_provider.py

Created by Scott on 2013-12-26.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import urllib
import urllib2

import grid_image_provider

from ice.logs import logger

class ConsoleGridProvider(grid_image_provider.GridImageProvider):

  @staticmethod
  def api_url():
    return "http://consolegrid.com/api/top_picture"

  @staticmethod
  def is_enabled():
    # TODO: Return True/False based on the current network status
    return True

  def consolegrid_top_picture_url(self, rom):
    host = self.api_url()
    quoted_name = urllib.quote(rom.name)
    return "%s?console=%s&game=%s" % (host, rom.console.shortname, quoted_name)

  def find_url_for_rom(self, rom):
    """
    Determines a suitable grid image for a given ROM by hitting
    ConsoleGrid.com
    """
    try:
      response = urllib2.urlopen(self.consolegrid_top_picture_url(rom))
      if response.getcode() == 204:
        name = rom.name
        console = rom.console.fullname
        logger.debug(
          "ConsoleGrid has no game called `%s` for %s" % (name, console)
        )
      else:
        return response.read()
    except urllib2.URLError as error:
      # Connection was refused. ConsoleGrid may be down, or something bad
      # may have happened
      logger.debug(
        "No image was downloaded due to an error with ConsoleGrid"
      )

  def download_image(self, url):
    """
    Downloads the image at 'url' and returns the path to the image on the
    local filesystem
    """
    (path, headers) = urllib.urlretrieve(url)
    return path

  def image_for_rom(self, rom):
    image_url = self.find_url_for_rom(rom)
    if image_url is None or image_url == "":
      return None
    return self.download_image(image_url)
