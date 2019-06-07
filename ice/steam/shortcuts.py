# encoding: utf-8
import vdf

import paths

from ice.steam._crc_algorithms import Crc
from steam import model


def shortcut_app_id(shortcut):
    """
    Generates the app id for a given shortcut. Steam uses app ids as a unique
    identifier for games, but since shortcuts dont have a canonical serverside
    representation they need to be generated on the fly. The important part
    about this function is that it will generate the same app id as Steam does
    for a given shortcut
    """
    algorithm = Crc(width=32, poly=0x04C11DB7, reflect_in=True, xor_in=0xffffffff, reflect_out=True, xor_out=0xffffffff)
    crc_input = ''.join([shortcut['Exe'], shortcut['AppName']])
    high_32 = algorithm.bit_by_bit(crc_input) | 0x80000000
    full_64 = (high_32 << 32) | 0x02000000
    return str(full_64)


# Helper functions which simply wrap the read/write shortcuts functions around
# the LocalUserContext object

def get_shortcuts(user_context):
    with open(paths.shortcuts_path(user_context), 'rb') as fp:
        vdf_dict = vdf.binary_loads(fp.read())
        return list(vdf_dict.get('shortcuts').values())


def set_shortcuts(user_context, shortcuts):
    # make the list of shortcuts under a nested "shortcuts" key with each index
    formatted_obj = {'shortcuts': {str(i): item for i, item in enumerate(shortcuts)}}
    byte_str = vdf.binary_dumps(formatted_obj)
    with open(paths.shortcuts_path(user_context), 'wb') as fp:
        fp.write(byte_str)

