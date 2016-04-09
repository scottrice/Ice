# encoding: utf-8

import webbrowser

from ice.logs import logger

class LaunchSteamTask(object):

  def __call__(self, app_settings, users, dry_run):
    # Use the `steam://` URL scheme registered with the OS to open Steam.
    # Bring them to the grid view of their games so they can appreciate
    # all of the pretty artwork.
    webbrowser.open_new("steam://nav/games/grid")
