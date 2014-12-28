#!/usr/bin/env python
# encoding: utf-8
"""
grid_image_provider.py

Created by Scott on 2013-12-26.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import abc


class GridImageProvider(object):

  def is_enabled(self):
    """
    Returns whether the GridImageProvider is available to use.
    """
    return True

  def image_for_rom(self, rom):
    """
    Returns a tuple of (image, error). If an image was found, 'image'
    should be the path of the image on disc and 'error' should be None. If
    no image was found, then 'image' should be None and error should be
    a subclass of 'StandardError'.
    """
    raise NotImplementedError("Not yet implemented")
