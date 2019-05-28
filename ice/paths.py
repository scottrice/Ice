# encoding: utf-8

import appdirs
import os

from steam.paths import user_config_directory


def application_data_directory():
  # Parameters are 'App Name' and 'App Author'
  # TODO: Get these values from the same place as setup.py
  return appdirs.user_data_dir("Ice", "Scott Rice")

def data_file_path(filename):
  return os.path.join(application_data_directory(), filename)

def archive_path():
  return data_file_path('archive.json')

def log_file_location():
  return data_file_path('ice.log')

def default_roms_directory():
  return os.path.join(os.path.expanduser('~'), 'ROMs')

def shortcuts_path(user_context):
  """Returns the path to the file in which Steam stores its shortcuts. This
  file is a custom file format, so see the `shortcuts` module if you would
  like to read/write to this file."""
  return os.path.join(
    user_config_directory(user_context),
    "shortcuts.vdf"
  )