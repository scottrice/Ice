"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import argparse

from pysteam.steam import get_steam

import decorators
import debug
import settings

from filesystem import RealFilesystem
from tasks import TaskEngine, SyncShortcutsTask, UpdateGridImagesTask

class CommandLineRunner(object):

  def __init__(self, steam=None, filesystem=None):
    self.steam = steam if steam is not None else get_steam()
    self.filesystem = RealFilesystem() if filesystem is None else filesystem

  def get_command_line_args(self, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('pdebug', type=bool, nargs='?', help="Pastes debug logs to pastebin to include with bug reports.")
    parser.add_argument('-s', '--skip-steam-check', action='store_true', help="Skips checking whether Steam is running")
    # Config options
    parser.add_argument('-c', '--config', type=str, default=None)
    parser.add_argument('-C', '--consoles', type=str, default=None)
    parser.add_argument('-e', '--emulators', type=str, default=None)
    # Debugging options
    parser.add_argument('-d', '--dry-run', action='store_true')
    return parser.parse_args(argv)

  def tasks_for_options(self, app_settings, options):
    return [
      SyncShortcutsTask(app_settings),
      UpdateGridImagesTask(app_settings),
    ]

  @decorators.catch_exceptions("An exception occurred while running Ice")
  def run(self, argv):
    options = self.get_command_line_args(argv[1:])

    if options.pdebug is True:
      debug.paste_debug_logs()
      return

    app_settings = settings.load_app_settings(self.filesystem, file_overrides = {
        'config.txt': options.config,
        'consoles.txt': options.consoles,
        'emulators.txt': options.emulators,
    })
    engine = TaskEngine(
      self.steam,
      filesystem = self.filesystem,
      app_settings = app_settings,
    )
    engine.run(
      tasks = self.tasks_for_options(app_settings, options),
      skip_steam_check=options.skip_steam_check,
      dry_run=options.dry_run
    )
