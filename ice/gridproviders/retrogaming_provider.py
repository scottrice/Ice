#!/usr/bin/env python
# encoding: utf-8
"""
retrogaming_provider.py

Created by Raphael on 2018-02-24.
"""

import sys
import os
import urllib
import urllib2

import grid_image_provider

from ice.logs import logger

class RetroGamingProvider(grid_image_provider.GridImageProvider):

  @staticmethod
  def api_url():
    return "http://retrogaming.cloud/api/v1/game/mostPopular"

  @staticmethod
  def is_enabled():
    # TODO: Return True/False based on the current network status
    return True

  def retrogaming_top_picture_url(self, rom):
    host = self.api_url()
    quoted_name = urllib.quote(rom.name)
    return "%s?console=%s&game=%s" % (host, rom.console.shortname, quoted_name)

  def find_url_for_rom(self, rom):
    """
    Determines a suitable grid image for a given ROM by hitting
    retrogaming.cloud
    """
    try:
      response = urllib2.urlopen(self.retrogaming_top_picture_url(rom))
      if response.getcode() == 204:
        name = rom.name
        console = rom.console.fullname
        logger.debug(
          "RetroGaming has no game called `%s` for %s" % (name, console)
        )
      else:
        return response.read()
    except urllib2.URLError as error:
      # Connection was refused. ConsoleGrid may be down, or something bad
      # may have happened
      logger.debug(
        "No image was downloaded due to an error with RetroGaming"
      )

  def download_image(self, url):
    """
    Downloads the image at 'url' and returns the path to the image on the
    local filesystem
    """
    try:
        (path, headers) = urllib.urlretrieve(url)
    except IOError as e:
        logger.debug('Unable to download image for %s', url)
        logger.error(e)
    return path

  def image_for_rom(self, rom):
    image_url = self.find_url_for_rom(rom)
    if image_url is None or image_url == "":
      return None
    return self.download_image(image_url)
