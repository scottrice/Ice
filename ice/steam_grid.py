#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2012-2013, 2013 Scott Rice
# All rights reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# SteamGridImageManager is meant to make setting the grid image of a given
# Steam shortcut super easy. Ideally, the user won't need to know anything
# about how steam grid images work, just mention the name and target and we
# will handle the rest
#

import os
import sys
import shutil
import crc_algorithms

class SteamGrid(object):
  
  def __init__(self,user_directory):
    """
    Sets up a SteamGridImageManager given the userdata directory for a given
    user.
    """
    self.user_directory = user_directory
    self.grid_image_directory = os.path.join(self.user_directory,"config","grid")
    # Make sure that the Grid Image directory exists
    if not os.path.exists(self.grid_image_directory):
        os.makedirs(self.grid_image_directory)
    
  def filename_for_shortcut(self,name,target):
    """
    Calculates the filename for a given shortcut. This filename is a 64bit
    integer, where the first 32bits are a CRC32 based off of the name and
    target (with the added condition that the first bit is always high), and
    the last 32bits are 0x02000000.
    """
    # This will seem really strange (where I got all of these values), but I
    # got the xor_in and xor_out from disassembling the steamui library for 
    # OSX. The reflect_in, reflect_out, and poly I figured out via trial and
    # error.
    algorithm = crc_algorithms.Crc(width = 32, poly = 0x04C11DB7, reflect_in = True, xor_in = 0xffffffff, reflect_out = True, xor_out = 0xffffffff)
    input_string = ''.join([target,name])
    top_32 = algorithm.bit_by_bit(input_string) | 0x80000000
    full_64 = (top_32 << 32) | 0x02000000
    return str(full_64)
    
  def filename_for_app(self,appid):
    """
    Calculates the filename for a given app. This is just the AppID
    """
    # Easy peasy
    return str(appid)
    
  def full_path_for_filename(self,filename,extension):
    """
    Returns the full, absolute, path to the shortcut. A shortcut is located in
    the userdata/{user_id}/config/grid/{generated_filename}.{extension}
    """
    filename_with_ext = "%s%s" % (filename,extension)
    return os.path.join(self.grid_image_directory,filename_with_ext)
    
  def existing_image_for_filename(self,filename):
    """
    Returns the path for an existing image. There are 4 possible paths an 
    existing image can be at, one for each extension. Returns the one that 
    actually exists
    """
    valid_exts = [".jpg",".jpeg",".png",".tga"]
    for ext in valid_exts:
      full_path = self.full_path_for_filename(filename,ext)
      if os.path.exists(full_path):
        return full_path
    return None
  
  def set_image_for_filename(self,image_path,filename):
    """
    Sets the image at 'image_path' to be the current application grid image for
    the given filename
    """
    # Delete the current image if there is one
    current_image = self.existing_image_for_filename(filename)
    if current_image:
      os.remove(current_image)
    # Set the new image
    _ , extension = os.path.splitext(image_path)
    grid_filepath = self.full_path_for_filename(filename,extension)
    # Copy the file
    shutil.copyfile(image_path,grid_filepath)
    
  def set_image_for_shortcut(self,image_path,name,target):
    """
    Sets the image at 'image_path' to be the current application grid image 
    for the shortcut defined by 'name' and 'target'
    """
    self.set_image_for_filename(image_path,self.filename_for_shortcut(name,target))
    
  def set_image_for_app(self,image_path,appid):
    """
    Sets the image at 'image_path' to be the current application grid image 
    for the app defined by 'appid'
    """
    self.set_image_for_filename(image_path,self.filename_for_app(appid))