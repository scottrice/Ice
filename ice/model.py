# encoding: utf-8

import collections

Console = collections.namedtuple('Console', [
  'fullname',
  'shortname',
  'extensions',
  'custom_roms_directory',
  'prefix',
  'icon',
  'images_directory',
  'emulator',
])

Emulator = collections.namedtuple('Emulator', [
  'name',
  'location',
  'format',
])