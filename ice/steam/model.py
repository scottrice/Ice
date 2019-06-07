# Represents a single shortcut on the user's machine. These are the 5 fields
# which are stored in shortcuts.vdf.
from pathlib import Path
from typing import NamedTuple


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
