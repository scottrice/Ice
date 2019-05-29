
# Represents a single shortcut on the user's machine. These are the 5 fields
# which are stored in shortcuts.vdf.
import re
from pathlib import Path
from typing import NamedTuple, Any, List


def parse_shortcuts_vdf(path):
    byte_slices = []
    with open(path, 'rb') as fp:
        read_byte = fp.read(1)
        # create a list of indices to slice all the shortcuts
        shortcut_offsets = []
        read_empty_byte = False
        read_shortcut_index = False
        while read_byte:
            if read_empty_byte and read_shortcut_index:
                shortcut_offsets.append(fp.tell())
                read_empty_byte = False
                read_shortcut_index = False
            elif read_byte == b'\x00':
                read_empty_byte = True
            elif read_empty_byte and re.match(rb'\d+', read_byte):
                read_shortcut_index = True
            else:
                read_empty_byte = False
                read_shortcut_index = False
            read_byte = fp.read(1)

        if not shortcut_offsets:
            return []
        offset = shortcut_offsets[0]
        fp.seek(offset)
        # read in slices of bytes if > 1 shortcuts
        for next_offset in shortcut_offsets[1:]:
            bytes_to_read = next_offset - offset
            byte_slices.append(fp.read(bytes_to_read))
            offset = next_offset
            fp.seek(offset)

        # finally read in the last slice, or first if there's only one shortcut
        byte_slices.append(fp.read())
    return [Shortcut.parse_from_bytes(byte_str) for byte_str in byte_slices]


class Shortcut(NamedTuple):
    name: str
    exe: str
    startdir: str
    icon: Any
    tags: List[str]

    @classmethod
    def parse_from_bytes(cls, byte_str: bytes):
        tokenized = byte_str.split(b'\x01')
        for pair in tokenized:
            try:
                if not pair:
                    continue

                key, value, *_ = pair.split(b'\x00')
                if key == b'AppName':
                    cls.name = value.decode()
                elif key == b'Exe':
                    temp = value.decode().strip('"')
                    # replace all instances of '" "'
                    cls.exe = temp.replace('" "', ' ')
                elif key == b'StartDir':
                    cls.startdir = value.decode().strip('"')
            except (UnicodeDecodeError, ValueError):
                pass
        return cls


# Represents a Steam installation. Since we don't really care about where the
# actual guts of Steam are located, the only property on this object is the
# location of the userdata directory (much more interesting).
class Steam(NamedTuple):
    userdata_directory: Path

# A simple composite object that encapsulates a local pysteam installation
# with a user id. Since basically everything that you would want pysteam to do
# is scoped within a single user on the system (set custom images, add/remove
# shortcuts, etc), most functions take this as a parameter so they dont need to
# take both a Steam installation and a user id.

class LocalUserContext(NamedTuple):
    steam: Steam
    user_id: int


