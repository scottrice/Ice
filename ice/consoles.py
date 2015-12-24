# encoding: utf-8

import os

def console_is_enabled(console):
  """Determines whether a console should have it's ROMs added to Steam."""
  return console.emulator is not None

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
