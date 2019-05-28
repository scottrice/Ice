# encoding: utf-8

import os

try:
  import winreg as registry
except ImportError:
  registry = None

def find_steam_location():
  """
  Finds the location of the current Steam installation on Windows machines.
  Returns None for any non-Windows machines, or for Windows machines where
  Steam is not installed.
  """
  if registry is None:
    return None

  key = registry.CreateKey(registry.HKEY_CURRENT_USER,"Software\Valve\Steam")
  return registry.QueryValueEx(key,"SteamPath")[0]

def find_userdata_directory():
  """
  Finds the location of the userdata directory on Windows machines. Returns
  None for any non-Windows machines, or for Windows machines where Steam is
  not installed.
  Since on Windows the userdata directory is simply a subdirectory of the
  installation directory, this function is really a thin wrapper over
  `find_steam_location`
  """
  install_location = find_steam_location()
  if install_location is None:
    return None

  return os.path.join(install_location, "userdata")