# encoding: utf-8

import appdirs
import os

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
