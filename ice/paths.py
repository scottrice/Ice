# encoding: utf-8

import appdirs

def application_data_directory():
  # Parameters are 'App Name' and 'App Author'
  # TODO: Get these values from the same place as setup.py
  return appdirs.user_data_dir("Ice", "Scott Rice")
