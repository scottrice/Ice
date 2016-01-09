#!/usr/bin/env python
# encoding: utf-8
"""
local_provider.py

Created by Scott on 2013-12-26.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import grid_image_provider

from ice.logs import logger

class LocalProvider(grid_image_provider.GridImageProvider):

  def valid_extensions(self):
    return ['.png', '.jpg', '.jpeg', '.tiff']

  def image_for_rom(self, rom):
    """
    Checks the filesystem for images for a given ROM. To do so, it makes
    use of a consoles 'images' directory. If it finds an image in that
    directory with the same name as the ROMs name then it will return that.
    """
    img_dir = rom.console.images_directory
    if img_dir == "":
      logger.debug(
        "[%s] No images directory specified for %s" %
        (rom.name, rom.console.shortname)
      )
      return None
    for extension in self.valid_extensions():
      filename = rom.name + extension
      path = os.path.join(img_dir, filename)
      if os.path.isfile(path):
        # We found a valid path, return it
        return path
    # We went through all of the possible filenames for this ROM and a
    # file didnt exist with any of them. There is no image for this ROM in
    # the consoles image directory
    return None
