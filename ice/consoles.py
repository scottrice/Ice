# encoding: utf-8

import os

import roms

def console_roms_directory(configuration, console):
  """
  If the user has specified a custom ROMs directory in consoles.txt then
  return that.

  Otherwise, append the shortname of the console to the default ROMs
  directory given by config.txt.
  """
  if console.custom_roms_directory:
    return console.custom_roms_directory
  return os.path.join(roms.roms_directory(configuration), console.shortname)

def path_is_rom(console, path):
  """
  This function determines if a given path is actually a valid ROM file.
  If a list of extensions is supplied for this console, we check if the path has a valid extension
  If no extensions are defined for this console, we just accept any file
  """
  if console.extensions == "":
    return True

  # Normalize the extension based on the things we validly ignore.
  # Aka capitalization, whitespace, and leading dots
  normalize = lambda ext: ext.lower().strip().lstrip('.')

  (name, ext) = os.path.splitext(path)
  valid_extensions = console.extensions.split(',')
  return normalize(ext) in map(normalize, valid_extensions)
