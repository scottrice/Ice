# encoding: utf-8

import paths

from ice.steam._crc_algorithms import Crc
from ice.steam._shortcut_generator import ShortcutGenerator
from ice.steam._shortcut_parser import ShortcutParser
from steam import shortcut_parser


def shortcut_app_id(shortcut):
  """
  Generates the app id for a given shortcut. Steam uses app ids as a unique
  identifier for games, but since shortcuts dont have a canonical serverside
  representation they need to be generated on the fly. The important part
  about this function is that it will generate the same app id as Steam does
  for a given shortcut
  """
  algorithm = Crc(width = 32, poly = 0x04C11DB7, reflect_in = True, xor_in = 0xffffffff, reflect_out = True, xor_out = 0xffffffff)
  crc_input = ''.join([shortcut.exe,shortcut.name])
  high_32 = algorithm.bit_by_bit(crc_input) | 0x80000000
  full_64 = (high_32 << 32) | 0x02000000
  return str(full_64)

# Helper functions which simply wrap the ShortcutGenerator and ShortcutParser
# APIs

def read_shortcuts(path):
  return ShortcutParser().parse(path)

def write_shortcuts(path, shortcuts):
  vdf_contents = ShortcutGenerator().to_string(shortcuts)
  with open(path, "w") as f:
    f.write(vdf_contents)

# Helper functions which simply wrap the read/write shortcuts functions around
# the LocalUserContext object

def get_shortcuts(user_context):
  shortcut_parser.parse_shortcuts(paths.shortcuts_path(user_context))
  return read_shortcuts(paths.shortcuts_path(user_context))

def set_shortcuts(user_context, shortcuts):
  write_shortcuts(paths.shortcuts_path(user_context), shortcuts)
