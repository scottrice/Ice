# encoding: utf-8
"""
This file contains an assortment of functions which deal with how Steam lays
out its directory hierarchy / where it places important files.
"""

import os

# =============================================================================
# Userdata paths
#
# These functions return the default userdata locations for OS X and Linux. On
# these two platforms the userdata directory doesn't change, so these functions
# are all you need to create a valid Steam instance. On Windows the userdata
# directory is stored in the installation directory, which could be anywhere.
# See the `winutils` module's `find_userdata_directory` function if you would
# like the path to the userdata directory on Windows.
#
# See also the `get_steam()` function, which will return a valid Steam
# instance for the current platform.

def default_osx_userdata_path():
  return os.path.join(
    os.path.expanduser("~"),
    "Library",
    "Application Support",
    "Steam",
    "userdata"
  )

def default_linux_userdata_path():
  return os.path.join(
    os.path.expanduser("~"),
    ".local",
    "share",
    "Steam",
    "userdata"
  )

# =============================================================================
# User-specific paths
#
# These functions all take a `user_context` parameter (an instance of the
# LocalUserContext class) and return various paths that are specific to that
# user. For example, this could be the location of that user's shortcuts.vdf
# file, or their `grid` directory (where custom images are stored)

def user_specific_data_directory(user_context):
  """Returns the subdirectory in `userdata` which acts as the root of the
  user-specific filesystem in Steam (aka all user-specific files are stored
  under this directory)"""
  return  os.path.join(
    user_context.steam.userdata_directory,
    user_context.user_id
  )

def user_config_directory(user_context):
  """Returns the user's config directory. This is normally not very useful,
  and consumers should look at `custom_images_directory` and `shortcuts_path`
  instead."""
  return os.path.join(
    user_specific_data_directory(user_context),
    "config"
  )

def custom_images_directory(user_context):
  """Returns the path to the directory in which Steam stores all of it's
  custom grid images. The images are stored where the name is the app id of
  the app whose image they want to override, and the extension is one of four
  valid extensions.

  See the `grid` module if you're interested in working with custom images"""
  return os.path.join(
    user_config_directory(user_context),
    "grid"
  )

def shortcuts_path(user_context):
  """Returns the path to the file in which Steam stores its shortcuts. This
  file is a custom file format, so see the `shortcuts` module if you would
  like to read/write to this file."""
  return os.path.join(
    user_config_directory(user_context),
    "shortcuts.vdf"
  )
