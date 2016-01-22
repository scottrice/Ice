# encoding: utf-8

import appdirs
import os

def application_data_directory():
  # Parameters are 'App Name' and 'App Author'
  # TODO: Get these values from the same place as setup.py
  return appdirs.user_data_dir("Ice", "Scott Rice")

def log_file_location():
  return os.path.join(application_data_directory(), 'ice.log')

def default_roms_directory():
  return os.path.join(os.path.expanduser('~'), 'ROMs')

def highest_precedent_data_file(filesystem, filename):
  """
  Returns the path to a data file named `filename`.
  This function first checks to see if the data file exists in the data
  directory. If so, it returns that.
  Then, this function checks to see if the data file exists in the local
  directory. If so, it returns that.
  If neither of those things are true then this function will return the
  path to a new file in the data directory.
  """
  local_path = os.path.abspath(filename)
  data_path = os.path.join(application_data_directory(), filename)
  if filesystem.is_file(data_path):
    return data_path
  elif filesystem.is_file(local_path):
    return local_path
  else:
    return data_path
