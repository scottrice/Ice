# encoding: utf-8

import os
import platform

from . import paths, winutils

from .model import LocalUserContext, Steam


def get_steam():
    """
    Returns a Steam object representing the current Steam installation on the
    users computer. If the user doesn't have Steam installed, returns None.
    """
    # Helper function which checks if the potential userdata directory exists
    # and returns a new Steam instance with that userdata directory if it does.
    # If the directory doesnt exist it returns None instead
    helper = lambda udd: Steam(udd) if os.path.exists(udd) else None

    # For both OS X and Linux, Steam stores it's userdata in a consistent
    # location.
    plat = platform.system()
    if plat == 'Darwin':
        return helper(paths.default_osx_userdata_path())
    if plat == 'Linux':
        return helper(paths.default_linux_userdata_path())

    # Windows is a bit trickier. The userdata directory is stored in the Steam
    # installation directory, meaning that theoretically it could be anywhere.
    # Luckily, Valve stores the installation directory in the registry, so its
    # still possible for us to figure out automatically
    if plat == 'Windows':
        possible_dir = winutils.find_userdata_directory()
        # Unlike the others, `possible_dir` might be None (if something odd
        # happened with the registry)
        return helper(possible_dir) if possible_dir is not None else None
    # This should never be hit. Windows, OS X, and Linux should be the only
    # supported platforms.
    # TODO: Add logging here so that the user (developer) knows that something
    # odd happened.
    return None


def local_user_ids(steam):
    """
    Returns a list of user ids who have logged into Steam on this computer.
    """
    if steam is None:
        return None
    # The userdata directory, at the top level, just contains a single
    # subdirectory for every user which has logged into this system (and
    # therefore that Steam has data for)
    return os.listdir(steam.userdata_directory)


def local_user_contexts(steam):
    if steam is None:
        return None
    return map(lambda uid: LocalUserContext(steam, uid), local_user_ids(steam))
